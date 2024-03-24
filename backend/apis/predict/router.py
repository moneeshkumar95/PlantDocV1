from fastapi import APIRouter, status, BackgroundTasks, HTTPException, Body, Query, Depends, File, UploadFile
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
import numpy as np


from apis.auth.utils import farmer_access, admin_access
from global_utils import success_response, convert_to_lower, CLASS_NAMES, MODEL, read_file_as_image
from global_models import UserTable, PredictionHistoryTable
from .utils import save_predication_history, get_predication_history_filters
from .schemas import PredicationHistorySchema


predict_router = APIRouter(prefix="/predict", tags=["Predict"])


@predict_router.post("")
def get_predication_API(
        background_task: BackgroundTasks,
        file: UploadFile = File(...),
        user_id=Depends(farmer_access)
):
    """
    API to user logout

    @param file: plant image
    @param background_task: BackgroundTasks
    @param user_id: int

    @return dict: success_response with species, class & accuracy
    """
    try:
        image = read_file_as_image(file.file.read())
        img_batch = np.expand_dims(image, 0)

        predictions = MODEL.predict(img_batch)

        species, predicted_class = CLASS_NAMES[np.argmax(predictions[0])].split("__")
        accuracy = int(np.max(predictions[0] * 100))

        results = {
            "species": species,
            "predicted_class": predicted_class,
            "accuracy": accuracy
        }

        background_task.add_task(
            save_predication_history,
            **user_id,
            **results
        )

        return success_response(
            detail="Plant image predicted successfully",
            data=results
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error predicting image"
        )


@predict_router.get("/predication-history")
def get_predication_history_API(
        filter_data: PredicationHistorySchema,
        background_task: BackgroundTasks,
        user_id=Depends(farmer_access)
) -> dict:
    """
    API to user logout

    @param filter_data: PredicationHistoryAdminSchema
    @param background_task: BackgroundTasks
    @param user_id: int

    @return dict: success_response with species, class & accuracy
    """
    try:
        filter_data = filter_data.dict()
        date = filter_data.pop("date")

        pk = Key("user_id").eq(user_id.get("id"))

        if date:
            pk &= Key("created_at").begins_with(date)

        filters = get_predication_history_filters(filter_data)

        prediction_history = PredictionHistoryTable.query(
            key=pk,
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
        