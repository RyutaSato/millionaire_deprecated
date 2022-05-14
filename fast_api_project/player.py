from typing import List
from card import Card


class Player:
    def __init__(self, ulid):
        self.__ulid = ulid
        self.cards: List[Card] = []
        self.score = 0

    def get_ulid(self):
        return self.__ulid

    def get_card_from_client_to_board(self) -> Card:
        # Clientから受け取る．
        # 整合性を調べる
        # 値を盤面に返す
        return self.cards.pop()

    def returned_invalid_card_from_board_to_player(self, card):
        self.cards.append(card)
