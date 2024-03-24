from fastapi import APIRouter, status, BackgroundTasks, HTTPException, Body, Query, Depends
from botocore.exceptions import ClientError


from apis.auth.utils import farmer_access
from global_utils import success_response, convert_to_lower
from global_models import UserTable
from .schemas import UpdateUserSchema


user_router = APIRouter(prefix="/user", tags=["User"])

@user_router.get("")
def get_user_API(
        user_id=Depends(farmer_access)
):
    try:
        user = UserTable.get(
            key={"id": user_id.get("id")}
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User no found"
            )
        user.pop("username", None)
        user.pop("hash_password", None)
        user.pop("user_type", None)
        user.pop("is_active", None)

        return success_response(
            detail="User data retrieved successfully",
            data=user
        )
    except ClientError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting user"
        )


@user_router.put("")
def get_user_API(
        update_data: UpdateUserSchema,
        user_id=Depends(farmer_access)
):
    try:
        user = UserTable.get(key=user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User no found"
            )

        filter_data = convert_to_lower(update_data.dict())

        for key, value in filter_data.items():
            user[key] = value

        UserTable.put(**user)

        return success_response(
            detail="User data updated successfully"
        )
    except ClientError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating user"
        )
