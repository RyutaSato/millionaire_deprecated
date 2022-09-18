# this is PLUGIN between Pydantic model and each Python object
from pydantic import BaseModel, validator
from uuid import UUID
from passlib.context import CryptContext
from datetime import datetime
PASSWORD_MAX = 63
PASSWORD_MIN = 8


# This file name will be named user.py
class UserModel(BaseModel):
    name: str

    class Config:
        orm_mode = True


class UserIn(UserModel):
    password: str

    def verify_password(self, hashed_password: str) -> bool:
        return CryptContext(schemes=["bcrypt"], deprecated="auto").verify(self.password, hashed_password)


class UserOut(UserModel):
    ulid: UUID
    created_at: datetime


class UserCreate(UserModel):
    password: str

    @validator('password')
    def validate_password_count(cls, law_password: str):
        if not PASSWORD_MIN <= len(law_password) <= PASSWORD_MAX:
            raise ValueError(f"password must be {PASSWORD_MIN} or over and {PASSWORD_MAX} or under.")
        return law_password
