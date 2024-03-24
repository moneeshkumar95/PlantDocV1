from fastapi import status
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr, Contains

from global_models import UserTable, PredictionHistoryTable

def save_predication_history(**kwargs):
    try:
        user_id = kwargs.pop("id")
        user = UserTable.get(
            key={"id": user_id},
            attributes_to_get="area, city, district, st, country, pincode"
        )

        predication_history_data = {**kwargs, **user, "user_id": user_id}
        PredictionHistoryTable.create(**predication_history_data)
    except ClientError as e:
        print(e)


def get_predication_history_filters(data):
    filters = None

    for key, value in data.items():
        filter_value = filters and value

        if filter_value:
            if key == "accuracy":
                filters &= Attr(key).eq(int(value))
            elif key == "user_id":
                filters &= Attr(key).eq(value)
            elif key == "date":
                filters &= Attr("created_at").begins_with(value)
            else:
                filters &= Attr(key).contains(value)
        elif value:
            if key == "accuracy":
                filters = Attr(key).eq(int(value))
            elif key == "user_id":
                filters = Attr(key).eq(value)
            elif key == "date":
                filters = Attr("created_at").begins_with(value)
            else:
                filters = Attr(key).contains(value)

    return filters
