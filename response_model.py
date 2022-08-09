from enum import Enum, auto
import datetime
from pydantic import BaseModel, Json, SecretStr


class ServerStatus(Enum):
    NORMAL = 'NORMAL'
    DELAY = 'DELAY'
    ERROR = 'ERROR'

    @staticmethod
    def check():
        return ServerStatus.NORMAL


class ClientStatus(Enum):
    LOGIN = 'LOGIN'
    LOGOUT = 'LOGOUT'
    PLAY = 'PLAY'

    @staticmethod
    def check():
        return ClientStatus.PLAY


class ResponseModelToClient(BaseModel):
    version: str = "0.1.0"
    server_status: ServerStatus = ServerStatus.check()
    server_time: str = datetime.datetime.now()[:-3]
    client_status: ClientStatus = ClientStatus.check()


class ResponseModelFromClient(BaseModel):
    pass


if __name__ == '__main__':
    rm = ResponseModelToClient()

    print(rm.json())
