import datetime

from fastapi import APIRouter, status, BackgroundTasks, HTTPException, Body, Query, Depends
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr, Contains

from apis.auth.schemas import RegisterSchema
from apis.auth.utils import add_user, admin_access
from global_utils import success_response
from global_models import UserTable, PredictionHistoryTable
from apis.predict.utils import get_predication_history_filters
from .schemas import PredicationHistoryAdminSchema, PredicationHistorySchema
from .utils import get_user_filters


admin_router = APIRouter(prefix="/admin", tags=["Admin"])

@admin_router.post("/register")
def register_user_API(
        user_data: RegisterSchema,
        background_task: BackgroundTasks
) -> dict:
    """
    API to register a user/admin

    @param user_data: RegisterSchema
    @param background_task:

    @return dict: success_response
    """
    try:

        data = add_user(user_data, background_task, is_admin=True)

        return success_response(
            detail="User registered successfully",
            data=data
        )
    except ClientError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error registering user"
        )


@admin_router.put("/activate-deactivate-user")
def activate_deactivate_user_API(
        data: dict = Body(...),
        admin_user_id=Depends(admin_access)
) -> dict:
    """
    API to register a user/admin

    @param data: User ID

    @return dict: success_response
    """
    try:
        user_id = data.get("id")

        user = UserTable.get(key={"id": user_id})

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        is_active = not user.get("is_active")
        user["is_active"] = is_active
        user_status = "activated" if is_active else "deactivated"

        UserTable.put(**user)

        return success_response(
            detail=f"User {user_status} successfully"
        )
    except ClientError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred during activation"
        )


@admin_router.get("/users")
def get_user_list_API(
    filter_data: PredicationHistorySchema,
    admin_user_id=Depends(admin_access)
):
    """
    API to get user list

    @param filter_data: PredicationHistorySchema
    @param admin_user_id: User ID

    @return dict: success_response
    """
    try:
        filters = get_user_filters(filter_data.dict())

        user_list = UserTable.scan(
            filters=filters,
            attributes_to_get="id, username, full_name, user_type, is_active, created_at"
        )

        return success_response(
            detail="User list retrieved successfully",
            data=user_list["Items"]
        )
    except ClientError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred during activation"
        )



@admin_router.delete("/user")
def delete_user_API(
    data: dict = Body(...),
    admin_user_id=Depends(admin_access)
):
    """
    API to delete user

    @param data:
    @param admin_user_id: User ID

    @return dict: success_response
    """
    try:
        user_id = data.get("id")
        user_list = UserTable.delete(key={"id": user_id})

        return success_response(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="User deleted successfully"
        )
    except ClientError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred during activation"
        )


@admin_router.get("/predication-history")
def get_predication_history_API(
        filter_data: PredicationHistoryAdminSchema,
        background_task: BackgroundTasks,
        user_id=Depends(admin_access)
) -> dict:
    """
    API to user logout

    @param filter_data: PredicationHistoryAdminSchema
    @param background_task: BackgroundTasks
    @param user_id: int

    @return dict: success_response with species, class & accuracy
    """
    try:
        filters = get_predication_history_filters(filter_data.dict())

        prediction_history = PredictionHistoryTable.scan(
            filters=filters
        )["Items"]

        return success_response(
            detail="Predication history retrieved successfully",
            data=prediction_history
        )
    except ClientError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting user"
        )
