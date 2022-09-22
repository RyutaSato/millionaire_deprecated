from pydantic import BaseModel, validator
from datetime import datetime, timedelta
from fast_api_project.card import Card
from fast_api_project.player import Player
from uuid import UUID
import ulid
import logging

logger = logging.getLogger(__name__)

"""
基本方針：
    Inでは、errorフラグが立っているときのみ受け付けるModelをErrorHandleModelに切り替え、
    それ以外の場合は期待したModelでのみ受け付ける。
"""


class WebSocketIn(BaseModel):
    sent_at: datetime
    error: bool = False

    def ping(self) -> timedelta:
        return datetime.now() - self.sent_at


class WebSocketOut(BaseModel):
    # WebSocket sending Model inherits this class
    obj_id: UUID = ulid.new().uuid
    sent_at: datetime = datetime.now()


class ErrorHandleModel(WebSocketIn):
    @validator("error")
    def check_error_flag(self):
        if not self.error:
            logger.error("An instance of ErrorHandleModel class was created even though no error flag was set")
            ValueError()


class UserStatusChangedNotify(WebSocketOut):
    pass


class BoardAllStatusNotify(WebSocketOut):
    discards: list[Card]
    players: list[Player]
    cards: list[Card]
