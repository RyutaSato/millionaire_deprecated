from enum import Enum

from pydantic import BaseModel, validator
from datetime import datetime, timedelta
from fast_api_project.card import Card
import logging

logger = logging.getLogger(__name__)

"""
基本方針：
    Inでは、errorフラグが立っているときのみ受け付けるModelをErrorHandleModelに切り替え、
    それ以外の場合は期待したModelでのみ受け付ける。
"""


class WebSocketIn(BaseModel):
    sent_at: datetime = datetime.now()
    error: bool = False

    def ping(self) -> timedelta:
        return datetime.now() - self.sent_at

    class Config:
        use_enum_values = True


class ErrorHandleModelIn(WebSocketIn):
    @validator("error")
    def check_error_flag(cls):
        if not cls.error:
            logger.error("An instance of ErrorHandleModel class was created even though no error flag was set")
            ValueError()


class PlayerCommandEnum(Enum):
    skip = "skip"
    pull = "pull"
    give = "give"


class PlayerSelectedCardsIn(WebSocketIn):
    """
    param:
        operation: PlayerCommandEnum
    """
    command: PlayerCommandEnum
    cards: list[Card]


class LobbyCommandEnum(Enum):
    UPDATING = "updating"
    QUEUE_IN = "queue_in"
    QUEUE_CANCEL = "queue_cancel"


class SelectedLobbyCommandIn(WebSocketIn):
    """
    param:
        command: LobbyCommandEnum
    """
    command: LobbyCommandEnum


class AdmittedModelsIn:
    def __init__(self):
        self.err_handle = ErrorHandleModelIn
        self.admitted_models: list = [PlayerSelectedCardsIn, SelectedLobbyCommandIn]

    def convert_from_str(self, msg: str):
        for admitted_model in self.admitted_models:
            try:
                return admitted_model.parse_raw(msg)
            except TypeError:
                logger.debug(f"{admitted_model} is invalid and skipped")
        return None

    def convert_from_dict(self, dct: dict):
        for admitted_model in self.admitted_models:
            try:
                return admitted_model(**dct)
            except TypeError:
                logger.debug(f"{admitted_model} is invalid and skipped")
        return None

    def test_selected_cards_in_from_str(self,
                                        card_str: str,
                                        command: PlayerCommandEnum = PlayerCommandEnum.pull
                                        ) -> PlayerSelectedCardsIn:
        sent_at = datetime.now()
        card = Card.retrieve_from_str(card_str)
        return PlayerSelectedCardsIn(sent_at=sent_at,
                                     command=command,
                                     cards=[card])
