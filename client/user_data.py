import asyncio
import logging
from asyncio import Event
from datetime import datetime

from fast_api_project.card import Card
from types_both import UserStatusType

logger = logging.getLogger(__name__)


def logger_change_user_data(attr, before, after):
    logger.info(f"{attr} was changed from'{before}' to '{after}'")


class UserData:
    def __init__(self):
        self._number: int = -1
        self._cards: list[Card] = []
        self._field: list[Card] = []  # 次に出すカードの判定に用いる。
        self._discards: list[Card] = []
        self._players: list[int] = []
        self.flag_my_turn: Event | None = None
        self.flag_end: Event | None = None
        self.time_out: datetime | None = None

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, new_num):
        logger_change_user_data("number", self._number, new_num)
        self._number = new_num

    def pull_cards(self, selected_cards: list[Card], am_i: bool):
        if am_i:
            for nt_card in selected_cards:
                for i in range(len(self._cards)):
                    if self._cards[i] == nt_card:
                        self._cards.pop(i)
                        break
            logger_change_user_data("cards", self._cards, selected_cards)
        logger_change_user_data("field", self._field, selected_cards)
        self._field = selected_cards

    def choice_one_card(self) -> list[Card]:
        if self._field:
            min_card = min(self._field)
            for tmp_card in self._cards:
                if tmp_card > min_card:
                    return [tmp_card]
            return []
        return [self._cards[0]]
