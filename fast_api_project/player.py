from fast_api_project.card import Card
import ulid
from uuid import UUID
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)


class Player(BaseModel):
    ulid_: UUID
    name: str = "user_name"
    cards: list[Card] = []

    @property
    def card_num(self) -> int:
        return int(len(self.cards))


if __name__ == '__main__':
    pass
