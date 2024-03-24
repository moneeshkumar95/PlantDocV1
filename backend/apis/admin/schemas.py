from pydantic import BaseModel
from typing import Optional


from apis.predict.schemas import PredicationHistorySchema


class PredicationHistoryAdminSchema(PredicationHistorySchema):
    user_id: Optional[str]


class PredicationHistorySchema(BaseModel):
    date: Optional[str]
    username: Optional[str]
    username: Optional[str]
    full_name: Optional[str]
    user_type: Optional[str]
    is_active: Optional[bool]
