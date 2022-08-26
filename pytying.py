from typing import Any

from fastapi import WebSocket
from pydantic import BaseModel, HttpUrl, SecretStr, datetime_parse, UUID4
# EmailStr
from secrets import token_urlsafe, token_bytes
from passlib.context import CryptContext
from datetime import datetime, timedelta
from uuid import uuid4
# from asyncio import sleep
from time import sleep

class UserBase(BaseModel):
    ulid: UUID4
    name: str
    password: str
    expired_time: datetime
    token: str


class UserIn(BaseModel):
    name: str
    token: str


# email: EmailStr
# full_name: str | None = None

class UserInDB(BaseModel):
    name: str
    password: str


class UserOut(UserBase):
    name: str
    # email: EmailStr
    # full_name: str | None = None


def create_user(name: str, law_password: str) -> UserBase:
    password = CryptContext(schemes=["bcrypt"], deprecated="auto").hash(law_password)
    expired_time = datetime.now() + timedelta(days=8)
    sleep(1)
    # :TODO DBにアクセス
    return UserBase(
        name=name,
        password=password,
        expired_time=expired_time,
        ulid=uuid4(),
        token=token_urlsafe(32)
    )


def signin_user(name: str, law_password: str) -> UserIn:
    # :TODO this class will be async
    sleep(1)
    hashed_password = "$2b$12$ZcfQp655Q2q7U47JiUPXz.kyUd9OtXs9u18on/bLxXv.5s090Amr6"
    if not CryptContext(schemes=["bcrypt"], deprecated="auto").verify(law_password, hashed_password):
        raise Exception()
    return UserIn(name=name, token=token_urlsafe(32))

import psycopg2
from sqlalchemy import create_engine
if __name__ == '__main__':
    conn = psycopg2.connect("dbname=postgres user=postgres password=secret host=localhost port=5432")
    PORT = 3452
    db = create_engine()
    # NAME = 'rsato'
    # PASSWORD = 'password'
    # user_base = create_user(NAME, PASSWORD)
    # print(user_base.json())
    # user_in = signin_user(NAME, PASSWORD)
    # print(user_in.json())
