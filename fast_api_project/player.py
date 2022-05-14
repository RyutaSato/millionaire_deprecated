from typing import List
from card import Card
import ulid

class Player:
    def __init__(self, ulid_:str):
        self._ulid: ulid.ULID = ulid.from_str(ulid_)
        self.cards: List[Card] = []
        self.score = 0

    def get_ulid(self):
        """
        >>> p = Player('01G2VKC7GNTAE57SA65BCP3V70')
        >>> p.get_ulid().str
        '01G2VKC7GNTAE57SA65BCP3V70'
        """
        return self._ulid

    def get_card_from_client_to_board(self) -> Card:
        # Clientから受け取る．
        # 整合性を調べる
        # 値を盤面に返す
        return self.cards.pop()

    def returned_invalid_card_from_board_to_player(self, card):
        self.cards.append(card)

if __name__ == '__main__':
    import doctest
    doctest.testmod()