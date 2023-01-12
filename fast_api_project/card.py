import logging
import re
from enum import Enum
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# TODO configファイルに移動する
from uuid import UUID

SUITE_LIST = ["jo", "sp", "cl", "di", "he"]
MAX_STRENGTH = 100
REGEX_CARD = r"(^jo0$)|(^(sp|cl|di|he)(0|1|2|3|4|5|6|7|8|9|11|12|13)$)"
pattern = re.compile(REGEX_CARD)


def create_from_str(string: str):
    """
    Validate `string` and returns a card class.
    Args:
        string (str): The string must be one of "sp", "cl", "di" and "he", and a number from 0 to 13, or "jo0".
    Returns:
        Card: Description of return value
    Raises:
        ValueError: If `string` doesn't match any patterns.
    """
    if pattern.match(string):
        su, num = pattern.match(string).groups()
        num = int(num)
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


class Card:
    """

    Args:
        suite: CardSuite
        number: CardNumber
        _strength: int
    """

    def __init__(self, **data):
        self.suite: CardSuite = data["suite"]
        self.number: CardNumber = data["number"]
        if "strength" in data.keys():
            self._strength: int = data["strength"]
        else:
            self._strength: int = self.set_strength(data["number"])

    @classmethod
    def create_from_str(cls, string: str):
        if not pattern.match(string):
            raise ValueError("string doesn't match any patterns")
        su, num = pattern.match(string).groups()
        num = int(num)
        if (su == "jo" and int(num) == 0) or (su != "jo" and 0 < num < 14):
            return cls(suite=CardSuite(su),
                       number=CardNumber(num),
                       )

    def __str__(self):
        return f"{self.suite.value}{self.number.value}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, Card):
            raise ValueError(f"{type(other)} is invalid")
        return self._strength == other._strength

    def __lt__(self, other):
        if not isinstance(other, Card):
            raise ValueError(f"{type(other)} is invalid")
        return self._strength < other._strength

    def __ne__(self, other):
        return not self.__eq__(other)

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __add__(self, other):
        if not isinstance(other, int):
            ValueError("'__add__' method must be integer")
        return Card(suite=self.suite, number=self.number, strength=self._strength + other)

    @staticmethod
    def set_strength(num: int | CardNumber) -> int:
        """

        Args:
            num:

        Returns:

        """
        # カードの強さはCard class内で定義されるべきではない？？
        if not isinstance(num, int):
            num: int = num.value
        if 0 < num < 14:
            return (num + 10) % 13
        return MAX_STRENGTH


if __name__ == "__main__":
    from fast_api_project.board import Board
    for _ in range(10):
        board = Board.test_init()
        for player in board.players:
            logger.debug(player.name)
            logger.debug(f"sequence pair: {player.cards.lookfor_sequence()}")
            logger.debug(f"equal pair: {player.cards.lookfor_equal()}")
            logger.debug("------------------------------------")
        board.test_run()
    # print(bytearray(str(cards).encode(encoding='utf-8')))
