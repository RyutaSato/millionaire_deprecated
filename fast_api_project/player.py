from typing import List
from card import Card


class Player:
    def __init__(self, ulid):
        self.__ulid = ulid
        self.cards: List[Card] = []
        self.score = 0

    def get_ulid(self):
        return self.__ulid

    def put_out(self) -> Card:
        return self.cards.pop()

    def returned_invalid_card(self, card):
        self.cards.append(card)
