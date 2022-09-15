from fastapi import WebSocket
from pydantic import BaseModel  # , EmailStr
from secrets import token_urlsafe


# This program is duplicated.
# UserOrm Model will be changed to user_base.py

class User:

    def __init__(self, websocket: WebSocket, name):
        self.ws = websocket
        self.name = name
        self.token = token_urlsafe(32)  # 256 bits are necessary and sufficient


class UserIn(BaseModel):
    username: str
    password: str
    # email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    # email: EmailStr
    full_name: str | None = None
