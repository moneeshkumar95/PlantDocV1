from bcrypt import hashpw, checkpw, gensalt
from jwt.exceptions import PyJWTError


import datetime
import uuid


from global_utils import db_resource, convert_to_lower


def generate_uuid() -> dict:
    """
    Generating the string type UUID

    :return: UUID in string
    """
    return {"id": str(uuid.uuid4())}


def generate_time() -> dict:
    """
    Generating the string type datetime

    :return: UUID in string
    """
    string_now = str(datetime.datetime.now())
    return {"created_at": string_now, "updated_at": string_now}


class BaseModel:
    def __init__(self, table_name):
        self.table = db_resource.Table(table_name)

    def get(self, key, attributes_to_get: bool = False):
        get_params = {"Key": key}

        if attributes_to_get:
            get_params["ProjectionExpression"] = attributes_to_get

        response = self.table.get_item(**get_params)
        return response.get('Item')

    def create(self, **item_data):
        item_data = {**generate_time(), **item_data}
        self.put(**item_data)
        return item_data

    def put(self, **item_data):
        self.table.put_item(Item=item_data)
        return item_data

    def delete(self, key):
        response = self.table.delete_item(Key=key)
        return response

    def query(
            self, key, filters=None, index: str = None, limit: int = None,
            start_key: dict = None, attributes_to_get: str = None, reverse: bool = False
    ):
        query_params = {"KeyConditionExpression": key, "ScanIndexForward": reverse}

        if filters:
            query_params["FilterExpression"] = filters

        if index:
            query_params["IndexName"] = index

        if limit:
            query_params["Limit"] = limit

        if start_key:
            query_params["ExclusiveStartKey"] = start_key

        if attributes_to_get:
            query_params["ProjectionExpression"] = attributes_to_get

        response = self.table.query(**query_params)
        return response

    def scan(
            self, filters=None, index: str = None, limit: int = None,
            start_key: dict = None, attributes_to_get: str = None
    ):
        scan_params = {}

        if filters:
            scan_params["FilterExpression"] = filters

        if index:
            scan_params["IndexName"] = index

        if limit:
            scan_params["Limit"] = limit

        if start_key:
            scan_params["ExclusiveStartKey"] = start_key

        if attributes_to_get:
            scan_params["ProjectionExpression"] = attributes_to_get

        response = self.table.scan(**scan_params)
        return response


class UserBase(BaseModel):
    ADMIN = "admin"
    FARMER = "farmer"

    USERNAME_INDEX = "username-index"

    def __init__(self):
        super().__init__('user')

    def create(self, **item_data):
        item_data = convert_to_lower(item_data)
        plain_password = item_data.pop("password", "")
        hash_password = hashpw(plain_password.encode("utf-8"), gensalt(13))

        item_data["hash_password"] = hash_password.decode("utf-8")
        updated_data = {**generate_uuid(), **item_data}

        return super().create(**updated_data)

    @staticmethod
    def verify_password(original_password, plain_password):
        return checkpw(password=plain_password.encode('utf-8'),
                       hashed_password=original_password.encode('utf-8'))


class BlacklistBase(BaseModel):
    def __init__(self):
        super().__init__('blacklist')

    def check_blacklist(self, jti):
        if super().get({"jti": jti}):
            raise PyJWTError()

class PredictionHistoryBase(BaseModel):
    def __init__(self):
        super().__init__('prediction_history')


# Create instances of the models
UserTable = UserBase()
BlacklistTable = BlacklistBase()
PredictionHistoryTable = PredictionHistoryBase()
