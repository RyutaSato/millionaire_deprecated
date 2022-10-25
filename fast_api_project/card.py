import logging
import re
from dataclasses import field

from pydantic import BaseModel, PrivateAttr
from enum import Enum
from random import shuffle

logger = logging.getLogger(__name__)
SUITE_LIST = ["jo", "sp", "cl", "di", "he"]
MAX_STRENGTH = 100
REGEX_CARD = r"^(jo|sp|cl|di|he)(0|1|2|3|4|5|6|7|8|9|11|12|13)$"
pattern = re.compile(REGEX_CARD)


def create_from_str(string: str):
    if pattern.match(string):
        su, num = pattern.match(string).groups()
        num = int(num)
        if (su == "jo" and int(num) == 0) or (su != "jo" and 0 < num < 14):
            return Card(suite=CardSuite(su),
                        number=CardNumber(num),
                        _strength=Card.set_strength(num))
    raise ValueError("string doesn't match any patterns")


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
        _strength: int
    """
    suite: CardSuite
    number: CardNumber
    _strength: int = PrivateAttr()

    # @property
    # def alias(self):
    #     return f"{self._suite}{self._number}"
    #

    def __init__(self, **data):
        super().__init__(**data)
        self._strength = self.set_strength(data["number"])

    #
    # def json(self, *args, **kwargs) -> str:
    #     return self.__str__()

    # @classmethod
    # def parse_raw(cls, string: str, *args, **kwargs):
    #     return cls.create_from_str(string)

    @classmethod
    def create_cards(cls, is_shuffle: bool = True, joker_num: int = 2):
        cards: list[Card] = []
        for _ in range(joker_num):
            cards.append(cls(suite=CardSuite("jo"), number=CardNumber(0)))
        for su in SUITE_LIST[1:]:
            for num in range(1, 14):
                cards.append(cls(suite=CardSuite(su), number=CardNumber(num)))
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
                           # strength=cls.set_strength(num)
                           )
        raise ValueError("string doesn't match any patterns")

    # def __setattr__(self, key, val):
    #     method = self.__config__.property_set_methods.get(key)
    #     if method is None:
    #         super().__setattr__(key, val)
    #     else:
    #         getattr(self, method)(val)

    def __str__(self):
        return f"{self.suite}{self.number}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, Card):
            raise NotImplementedError
        return self._strength == other._strength

    def __lt__(self, other):
        if not isinstance(other, Card):
            raise NotImplementedError
        return self._strength < other._strength

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
    def set_strength(num: int | CardNumber):
        if type(num) != int:
            num = num.value
        if 0 < num < 14:
            return (num + 10) % 13
        return MAX_STRENGTH

    class Config:
        use_enum_values = True
        # property_set_methods = {"coords": "set_coords"}


if __name__ == "__main__":
    class Cards(BaseModel):
        cards: list[Card] = Card.create_cards()


    cards = Cards()
    print(len(bytearray(str(cards.json()).encode(encoding='utf-8'))))
    print(cards.json())
    print(Cards.parse_raw(cards.json()))
