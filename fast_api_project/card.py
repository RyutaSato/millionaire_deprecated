import logging
from typing import List

logger = logging.getLogger(__name__)


class CardFunc:
    def func_skip(self):
        pass


class Card(CardFunc):
    def __init__(self, suit='nul', mark='?', order=-1, strength=-1, func_names: List[str] = List[str]):
        self.suit = suit
        self.mark = mark
        self.order = order
        self.strength = strength
        self.functions = []
        for func_name in func_names:
            func = getattr(Card, func_name)
            if func is not None:
                self.functions.append(func)

    def __str__(self):
        return f"{self.suit}:{self.strength}"

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
        logger.info(f'deleted Card {self.suit} {self.order}')