from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel
import ulid

from fast_api_project.card import Card
from fast_api_project.player import Player


class CommandOutEnum(Enum):
    UserStatusChanged = "USC"
    BoardAllStatus = "BAS"


class WebSocketOut(BaseModel):
    # WebSocket sending Model inherits this class
    sent_at: datetime = datetime.now()
    command: CommandOutEnum

    class Config:
        use_enum_values = True


class UserStatusChangedOut(WebSocketOut):
    command = CommandOutEnum.UserStatusChanged


class BoardAllStatusOut(WebSocketOut):
    command = CommandOutEnum.BoardAllStatus
    discards: list[Card]
    players: list[Player]
    cards: list[Card]
