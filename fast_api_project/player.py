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
    def test_create_player(case: int):
        if case == 1:
            return Player(ulid=UUID("01835c3a-fb3d-b4e2-a43e-1682dc0be131"), name="test1")
        elif case == 2:
            return Player(ulid=UUID("01835c3a-fb3d-832f-27eb-0126cee681e9"), name="test2")
        elif case == 3:
            return Player(ulid=UUID("01835c3a-fb3d-1c2e-8375-a475a429ca89"), name="test3")
        return Player(ulid=UUID("01835c3a-fb3d-3520-3d79-6534542003b1"), name="test4")


if __name__ == '__main__':
    pass
