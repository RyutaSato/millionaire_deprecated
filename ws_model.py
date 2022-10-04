from enum import Enum

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

    class Config:
        use_enum_values = True


class WebSocketOut(BaseModel):
    # WebSocket sending Model inherits this class
    obj_id: UUID = ulid.new().uuid
    sent_at: datetime = datetime.now()

    class Config:
        use_enum_values = True


class ErrorHandleModelIn(WebSocketIn):
    @validator("error")
    def check_error_flag(cls):
        if not cls.error:
            logger.error("An instance of ErrorHandleModel class was created even though no error flag was set")
            ValueError()


class UserStatusChangedOut(WebSocketOut):
    pass


class BoardAllStatusOut(WebSocketOut):
    discards: list[Card]
    players: list[Player]
    cards: list[Card]


class PlayerOperationEnum(Enum):
    skip = "skip"
    pull = "pull"
    give = "give"


class SelectedCardsIn(WebSocketIn):
    operation: PlayerOperationEnum
    cards: list[Card]


class LobbyCommandEnum(Enum):
    QUEUE_IN = "queue_in"
    QUEUE_CANCEL = "queue_cancel"


class SelectedLobbyCommandIn(WebSocketIn):
    command: LobbyCommandEnum


class AdmittedModelsIn:
    def __init__(self):
        self.err_handle = ErrorHandleModelIn
        self.admitted_models: list = [SelectedCardsIn, SelectedLobbyCommandIn]

    def convert_from_str(self, msg: str):
        for admitted_model in self.admitted_models:
            try:
                return admitted_model.parse_raw(msg)
            except TypeError:
                pass
        return None

    def convert_from_dict(self, dct: dict):
        pass

    def test_selected_cards_in_from_str(self, card_str: str, operation: PlayerOperationEnum) -> SelectedCardsIn:
        sent_at = datetime.now()
        operation = PlayerOperationEnum.pull
        card = Card.retrieve_from_str(card_str)
        return SelectedCardsIn(sent_at=sent_at,
                               operation=operation,
                               cards=[card])
