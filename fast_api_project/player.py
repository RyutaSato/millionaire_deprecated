from fast_api_project.card import Card
import ulid
from uuid import UUID
from pydantic import BaseModel
import logging

from fast_api_project.cards import Cards

logger = logging.getLogger(__name__)


class Player:
    def __init__(self, uuid: UUID, name: str):
        self.uuid = uuid
        self.name = name
        # self.connection_status = ???
        self.cards = Cards()
        self.passed = False

    def __len__(self):
        return self.cards.__len__()

    def play_cards(self, played_cards: list[Card] | None):
        candidate_cards_set = self.cards.lookfor_candidate_cards_set(played_cards)
        if candidate_cards_set:
            return candidate_cards_set[0]
        return []


if __name__ == '__main__':
    pass
