import logging
import re
from pydantic import BaseModel
from enum import Enum
from random import shuffle

logger = logging.getLogger(__name__)
SUITE_LIST = ["jo", "sp", "cl", "di", "he"]
MAX_STRENGTH = 100
REGEX_CARD = r"^(jo|sp|cl|di|he)(0|1|2|3|4|5|6|7|8|9|11|12|13)$"
pattern = re.compile(REGEX_CARD)


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
    """
    params:
        suite: CardSuite
        number: CardNumber
        strength: int
    """
    suite: CardSuite
    number: CardNumber
    strength: int

    @classmethod
    def create_cards(cls, is_shuffle: bool = True, joker_num: int = 2):
        cards: list[Card] = []
        for _ in range(joker_num):
            cards.append(cls(suite=CardSuite("jo"), number=CardNumber(0), strength=MAX_STRENGTH))
        for su in SUITE_LIST[1:]:
            for num in range(1, 14):
                cards.append(cls(suite=CardSuite(su), number=CardNumber(num), strength=cls.set_strength(num)))
        if is_shuffle:
            shuffle(cards)
        return cards

    @classmethod
    def create_from_str(cls, string: str):
        if pattern.match(string):
            su, num = pattern.match(string).groups()
            num = int(num)
            if (su == "jo" and int(num) == 0) or (su != "jo" and 0 < num < 14):
                return cls(suite=CardSuite(su),
                           number=CardNumber(num),
                           strength=cls.set_strength(num))
        raise ValueError("string doesn't match any patterns")

    def __str__(self):
        return f"{self.suite}{self.number}"

    def __eq__(self, other):
        if not isinstance(other, Card):
            raise NotImplementedError
        return self.strength == other.strength

    def __lt__(self, other):
        if not isinstance(other, Card):
            raise NotImplementedError
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
        if 0 < num < 14:
            return (num + 10) % 13
        return MAX_STRENGTH

    class Config:
        use_enum_values = True
