from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError 
from bcrypt import hashpw, checkpw, gensalt


import datetime


from global_utils import success_response
from global_models import UserTable
from .schemas import RegisterSchema, LoginSchema, PasswordChangeSchema
from .utils import (
    create_access_token, auth_required, get_current_user, save_location_details, user_log_out_bg,
    admin_access, farmer_access, add_user,
)

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register")
def register_user_API(
        user_data: RegisterSchema,
        background_task: BackgroundTasks
) -> dict:
    """
    API to register a user

    @param user_data: RegisterSchema
    @param background_task:

    @return dict: success_response with User ID & access token
    """
    try:

        add_user(user_data, background_task)

        return success_response(
            status_code=status.HTTP_201_CREATED,
            detail="User registered successfully",
        )
    except ClientError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error registering user"
        )


@auth_router.post("/login")
def user_login_API(
        login_data: LoginSchema
) -> dict:
    """
    API to user login

    @param login_data:

    @return dict: success_response with User ID & access token
    """
    try:
        user = UserTable.query(
            key=Key("username").eq(login_data.username),
            index=UserTable.USERNAME_INDEX,
            attributes_to_get="id, hash_password, user_type, created_at, full_name, is_active"
        )["Items"]

        credentials_exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials"
        )
        user = user[0]

        if not user:
            raise credentials_exception

        if not user.get("is_active"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your account is not activated, please contact administrator"
            )

        hash_password = user.get("hash_password")

        if not UserTable.verify_password(hash_password, login_data.password):
            raise credentials_exception

        access_token = create_access_token(
            data={
                "sub": user.get("id"),
                "role": user.get("user_type")
            }
        )

        data = {
            "id": user.get("id"),
            "access_token": access_token,
            "full_name": user.get("full_name"),
            "user_type":  user.get("user_type")
        }

        return success_response(
            detail="User logged-in successfully",
            data=data
        )
    except ClientError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred during login"
        )


@auth_router.delete("/logout")
def user_login_API(
        background_task: BackgroundTasks,
        token_data: dict = Depends(auth_required)
) -> dict:
    """
    API to user logout

    @param token_data:
    @param background_task:

    @return dict: success_response
    """
    try:
        background_task.add_task(user_log_out_bg, token_data)
        return success_response(
            detail="User logged-out successfully"
        )
    except ClientError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred during login"
        )


@auth_router.put("/password-change")
def get_user_API(
        data: PasswordChangeSchema,
        user_id=Depends(farmer_access)
):
    """
    API to user password change

    @param data: PasswordChangeSchema
    @param user_id: int

    @return dict: success_response
    """
    try:
        user = UserTable.get(key=user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User no found"
            )

        if not UserTable.verify_password(user.get("hash_password"), data.old_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid password"
            )

        hash_password = hashpw(data.password.encode("utf-8"), gensalt(13))

        user["hash_password"] = hash_password.decode("utf-8")

        UserTable.put(**user)

        return success_response(
            detail="Password changed successfully"
        )
    except ClientError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred during password change"
        )
