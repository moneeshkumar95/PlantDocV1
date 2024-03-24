from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import requests
import jwt
from jwt.exceptions import PyJWTError
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError


import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from settings import (
    JWT_SECRET_KEY, JWT_ALGORITHM, JWT_ACCESS_TOKEN_EXPIRE, GOOGLE_GEOCODE_BASE_URL, GOOGLE_API_KEY
)
from global_utils import str_to_datetime, db_resource
from global_models import UserTable, BlacklistTable


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/user/login")


def get_location_details(pincode) -> dict:
    """
    Helper function to get the geocode
    """
    location_details = {
        "area": None,
        "city": None,
        "district": None,
        "st": None,
        "country": None,
        "pincode": None
    }

    params = {
        "address": pincode,
        "key": GOOGLE_API_KEY
    }

    response = requests.get(GOOGLE_GEOCODE_BASE_URL, params=params)
    data = response.json()

    if data["status"] == "OK":
        result = data["results"][0]
        address_components = result["address_components"]

        for component in address_components:
            if "sublocality" in component["types"]:
                location_details["area"] = component["long_name"].lower()
            elif "locality" in component["types"]:
                location_details["city"] = component["long_name"].lower()
            elif "administrative_area_level_3" in component["types"]:
                location_details["district"] = component["long_name"].lower()
            elif "administrative_area_level_1" in component["types"]:
                location_details["st"] = component["long_name"].lower().replace(" ", "")
            elif "country" in component["types"]:
                location_details["country"] = component["long_name"].lower()
            elif "postal_code" in component["types"]:
                location_details["pincode"] = component["long_name"].lower()

    return location_details


def save_location_details(data) -> None:
    try:
        location_details = get_location_details(data.get("pincode"))

        if location_details.get("pincode"):
            for key, value in location_details.items():
                if value:
                    data[key] = value
        else:
            data.pop("pincode", None)

        UserTable.put(**data)
    except ClientError as e:
        print(e)


def add_user(user_data, background_task, is_admin: bool = False):
    is_active = True

    existing_user = UserTable.query(
        key=Key("username").eq(user_data.username),
        index=UserTable.USERNAME_INDEX,
        attributes_to_get="id"
    )["Items"]

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )
    user_data.user_type = UserTable.FARMER if not is_admin else user_data.user_type

    if not is_admin:
        user_data.user_type = UserTable.FARMER
        is_active = False

    user = UserTable.create(**user_data.dict(), is_active=is_active)

    access_token = create_access_token(
        data={
            "sub": user.get("id"),
            "role": user.get("user_type"),
        }
    )
    background_task.add_task(save_location_details, user)

    return {"id": user.get("id"), "access_token": access_token}

def create_access_token(data: dict) -> str:
    """
    For the generating the access_token or refresh_token

    :param data: sub-> user_id
    :return: JWT token
    """
    data.update(
        {
            "exp": datetime.utcnow() + JWT_ACCESS_TOKEN_EXPIRE,
            'jti': str(uuid.uuid4()),
            "type": "access"
        }
    )
    token = jwt.encode(data, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def user_log_out_bg(token_data):
    jti = token_data.get('jti')
    ttl = datetime.now(timezone.utc) + timedelta(days=30)
    BlacklistTable.put(jti=jti, ttl=str(ttl))


def auth_required(token: str = Depends(oauth2_scheme)) -> dict:
    """
    For checking the JWT token is valid

    :return: parsed token data
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Login expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        jti: str = payload['jti']
        BlacklistTable.check_blacklist(jti)
    except (PyJWTError, JWTError, KeyError):
        raise credentials_exception

    return payload


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    For checking the JWT token & get the current user data

    :return: User data
    """
    data = auth_required(token=token)
    user_id = data.get("sub")
    user = UserTable.get(key={"id": user_id})

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    return user


def admin_access(token: str = Depends(oauth2_scheme)):
    """
    For checking the JWT token & user type

    :return: User data
    """
    data = auth_required(token=token)
    role = data.get("role")

    if role != UserTable.ADMIN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not allowed")

    return {"id": data.get("sub")}


def farmer_access(token: str = Depends(oauth2_scheme)):
    """
    For checking the JWT token & user type

    :return: User data
    """
    data = auth_required(token=token)

    return {"id": data.get("sub")}
