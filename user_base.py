# this is PLUGIN between Pydantic model and each Python object
import ulid
from pydantic import BaseModel, UUID4
from secrets import token_urlsafe, token_bytes
from passlib.context import CryptContext
from datetime import datetime, timedelta
from time import sleep

# This file name will be named user.py
class UserBase(BaseModel):
    name: str
    expired_time: datetime
    token: str

    class Config:
        orm_mode = True


class UserIn(UserBase):
    password: str


class UserCreate(UserBase):
    password: str


class UserOut(BaseModel):
    name: str
    expired_time: datetime
    token: str
    # email: EmailStr
    # full_name: str | None = None


def create_userbase(name: str, law_password: str) -> UserCreate:
    password = CryptContext(schemes=["bcrypt"], deprecated="auto").hash(law_password)
    sleep(1)
    # :TODO DBにアクセス
    return UserCreate(
        name=name,
        password=password,
        expired_time=datetime.now() + timedelta(days=8),
        token=token_urlsafe(32)
    )


def authenticate_user(law_password: str, hashed_password: str) -> bool:
    # :TODO this class will be async
    if CryptContext(schemes=["bcrypt"], deprecated="auto").verify(law_password, hashed_password):
        return True
    return False
