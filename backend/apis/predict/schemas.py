from pydantic import BaseModel
from typing import Optional


class PredicationHistorySchema(BaseModel):
    date: Optional[str]
    species: Optional[str]
    predicted_class: Optional[str]
    accuracy: Optional[int]
    area: Optional[str]
    city: Optional[str]
    district: Optional[str]
    country: Optional[str]
    pincode: Optional[str]
