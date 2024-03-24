from pydantic import BaseModel
from typing import Optional


class UpdateUserSchema(BaseModel):
    full_name: Optional[str]
    email: Optional[str]
    area: Optional[str]
    city: Optional[str]
    district: Optional[str]
    st: Optional[str]
    country: Optional[str]
    pincode: Optional[str]


