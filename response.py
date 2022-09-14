from passlib.context import CryptContext
from pydantic import BaseModel, validator

PASSWORD_MAX = 63
PASSWORD_MIN = 8


class UserCreateResponseModel(BaseModel):
    name: str
    password: str

    @validator('password')
    def check_count(cls, law_password: str):
        if not PASSWORD_MIN <= len(law_password) <= PASSWORD_MAX:
            raise ValueError(f"password must be {PASSWORD_MIN} or over and {PASSWORD_MAX} or under.")
        return law_password


class LoginResponseModel(BaseModel):
    name: str
    password: str
