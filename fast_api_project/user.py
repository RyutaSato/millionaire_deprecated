from uuid import UUID

from fastapi.websockets import WebSocket

from fast_api_project.player import Player


class User:
    def __init__(self, token: str, ws: WebSocket, ):
        self.token = token
        self.ws = ws
        self.player = Player(
            ulid=UUID(token),
            name="test"
        )
