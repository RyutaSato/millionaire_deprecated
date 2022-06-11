from fastapi import WebSocket
from pydantic import BaseModel # , EmailStr


class User(BaseModel):

    def __init__(self, websocket: WebSocket, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ws = websocket
        self.name = name


class UserIn(BaseModel):
    username: str
    password: str
    # email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    # email: EmailStr
    full_name: str | None = None
