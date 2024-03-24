from pydantic import BaseModel, validator, Field, validators
from global_models import UserTable

from typing import Optional


class PasswordScheme(BaseModel):
    password: str


class LoginSchema(PasswordScheme):
    username: str


class RegisterSchema(LoginSchema):
    email: str
    full_name: str
    pincode: str = Field(..., min_length=6, max_length=6)
    user_type: Optional[str]

    @validator('user_type')
    def validate_user_type(cls, user_type):
        allowed_types = [UserTable.ADMIN, UserTable.FARMER]
        if user_type not in allowed_types:
            raise ValueError(f"Invalid user_type. Allowed values: {', '.join(allowed_types)}")
        return user_type


class PasswordChangeSchema(PasswordScheme):
    old_password: str
