import logging
from pydantic import BaseModel
from enum import Enum

logger = logging.getLogger(__name__)


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
    JOKER = 0
    SPADE = 1
    CLOVER = 2
    DIAMOND = 3
    HEART = 4


class Card(BaseModel):
    suite: CardSuite
    number: CardNumber
    strength: int

    def __str__(self):
        return f"{self.suite.name}{self.number.value}"

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


if __name__ == "__main__":
    li = []
    for suite in range(1, 5):
        for number in range(1, 14):
            li.append(Card(suite=suite, number=number, strength=Card.set_strength(number)))
    for i in li:
        print(i, end=" ")
    print()
