import logging

from fast_api_project.card import Card
from fast_api_project.player import Player
from ws_request_model import RqOpePullCards
from ws_types import UserStatusType, GameOperationType

logger = logging.getLogger(__name__)


class UserData:
    def __init__(self):
        self.name: str = "loading..."
        self.status: UserStatusType = UserStatusType.Lobby
        self.cards: list[Card] = []
        self.field: list[Card] = []  # 次に出すカードの判定に用いる。
        self.players: list[Player] = []

    def choice_one_card(self) -> list[Card]:
        if self.field:
            min_card = min(self.field)
            for tmp_card in self.cards:
                if tmp_card > min_card:
                    return [tmp_card]
            return []
        return [self.cards[0]]
