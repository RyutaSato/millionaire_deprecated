import logging

from fast_api_project.card import Card
from types_both import UserStatusType

logger = logging.getLogger(__name__)


def logger_change_user_data(attr, before, after):
    logger.info(f"{attr} was changed from'{before}' to '{after}'")


class UserData:
    def __init__(self):
        self._name: str = "loading..."
        self._number: int = -1
        self._status: UserStatusType = UserStatusType.Lobby
        self._cards: list[Card] = []
        self._field: list[Card] = []  # 次に出すカードの判定に用いる。
        self._discards: list[Card] = []
        self._players: list[int] = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name: str):
        logger_change_user_data("name", self._name, new_name)
        self._name = new_name

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, new_num):
        logger_change_user_data("number", self._number, new_num)
        self._number = new_num

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status: UserStatusType):
        logger_change_user_data("status", self._status.name, new_status.name)
        self._status = new_status

    # @property
    # def cards(self):
    #     return self._cards

    def pull_cards(self, selected_cards: list[Card], am_i: bool):
        if am_i:
            for nt_card in selected_cards:
                for i in range(len(self._cards)):
                    if self._cards[i] == nt_card:
                        self._cards.pop(i)
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
