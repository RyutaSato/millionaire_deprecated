from card import Card
import ulid
from uuid import UUID
from pydantic import BaseModel


class Player(BaseModel):
    ulid: UUID
    name: str
    cards: list[Card] = []

    def print_status(self):
        print("******* player: {0} name: {1} ********".format(self.ulid, self.name))
        for card in self.cards:
            print(card, end=", ")
        print()

    @staticmethod
    def test_create_player():
        return Player(ulid=ulid.new().uuid, name="test")


if __name__ == '__main__':
    pass
