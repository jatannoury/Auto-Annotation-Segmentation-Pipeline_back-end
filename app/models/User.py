from pydantic import BaseModel, validator
from typing import Optional
import re

class User(BaseModel):
    firstName: str
    lastName: str
    birthday: str; gender: str
    email: str
    password: str

    @validator('*')
    def enforce_non_empty(cls, value):
        if value is None:
            raise ValueError("Field cannot be None")
        if isinstance(value, str) and not value.strip():
            raise ValueError("Field cannot be empty")
        return value

    @validator('email')
    def validate_email(cls, value: str):
        if "@" not in value:
            raise ValueError("Email not in correct format")
        if ".com" not in value:
            raise ValueError("Email should contain Top level domain (TLD)")
        return value
    @validator("password")
    def validate_password(cls, value):
        regex_expression = "^(?=.*[A-Z]).{6,}$"
        if re.match(regex_expression, value) == False:
            raise ValueError("Password should be at least 6 characters and contain at least one upper case letter")
        return value