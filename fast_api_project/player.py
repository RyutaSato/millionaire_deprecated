from fast_api_project.card import Card
import ulid
from uuid import UUID
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

class Player(BaseModel):
    ulid: UUID
    name: str
    cards: list[Card] = []

    def print_status(self):
        logger.info("******* player: {0} name: {1} ********".format(self.ulid, self.name))
        cards_str = []
        for card in self.cards:
            cards_str.append(str(card))
        logger.info(", ".join(cards_str))


if __name__ == '__main__':
    pass
