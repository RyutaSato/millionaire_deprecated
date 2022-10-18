from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
import ulid

from fast_api_project.card import Card
from fast_api_project.player import Player


class WebSocketOut(BaseModel):
    # WebSocket sending Model inherits this class
    sent_at: datetime = datetime.now()

    class Config:
        use_enum_values = True


class UserStatusChangedOut(WebSocketOut):
    pass


class BoardAllStatusOut(WebSocketOut):
    discards: list[Card]
    players: list[Player]
    cards: list[Card]
