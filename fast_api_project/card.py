import logging
from pydantic import BaseModel
from enum import Enum
from random import shuffle

logger = logging.getLogger(__name__)
SUITE_LIST = ["jo", "sp", "cl", "di", "he"]


class CardNumber(Enum):
    NONE = 0
    ACE = 1
    DEUCE = 2
    TREY = 3
    CATER = 4
    CINQUE = 5
    SICE = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13


class CardSuite(Enum):
    # :TODO change suite values to suite strings
    JOKER = SUITE_LIST[0]
    SPADE = SUITE_LIST[1]
    CLOVER = SUITE_LIST[2]
    DIAMOND = SUITE_LIST[3]
    HEART = SUITE_LIST[4]


class Card(BaseModel):
    suite: CardSuite
    number: CardNumber
    strength: int

    @classmethod
    def create_cards(cls, is_shuffle: bool = True):
        cards: list[Card] = []
        for su in SUITE_LIST:
            for num in range(1, 14):
                cards.append(cls(suite=su, number=num, strength=(num + 10) % 13))
        if is_shuffle:
            shuffle(cards)
        return cards

    @classmethod
    def retrieve_from_str(cls, strings: str):
        str_cards = strings.split("&")
        cards: list[cls] = []
        for str_card in str_cards:
            if not str_card[2:].isnumeric() or not str_card[:2] in SUITE_LIST:
                logger.error("ValueError: {} includes a wrong value".format(strings))
                return []
            num = int(str_card[2:])
            if not 0 <= num <= 13:
                logger.error("ValueError: Invalid card number: {}".format(num))
                return []
            cards.append(cls(
                suite=str_card[:2],
                number=int(str_card[2:]),
                strength=cls.set_strength(int(str_card[2:]))
            ))
        return cards

    def __str__(self):
        return f"{self.suite}{self.number}"

    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.strength == other.strength

    def __lt__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.strength < other.strength

    def __ne__(self, other):
        return not self.__eq__(other)

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __del__(self):
        pass

    @staticmethod
    def set_strength(num: int):
        return (num + 10) % 13

    class Config:
        use_enum_values = True


# :TODO Move to test_card.py
if __name__ == "__main__":
    li = []
    for suite in SUITE_LIST[1:]:
        for number in range(1, 14):
            li.append(Card(suite=suite, number=number, strength=Card.set_strength(number)))
    for i in li:
        print(i.json(), end=" ")
    print()
    li = Card.retrieve_from_str("he13&sp8")
    for i in li:
        print(i.json())
