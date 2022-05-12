from typing import List
from user import User


class Card:
    def __init__(self, name: str, power: int, functions: List[str]):
        self.name = name
        self.power = power
        self.functions = []
        for func in functions:
            tmp = getattr(Card, func, "None")
            if tmp is not None:
                self.functions.append(tmp)

    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.power == other.power

    def __lt__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.power < other.power

    def __ne__(self, other):
        return not self.__eq__(other)

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)


class Gameboard:
    settings_DEFAULT = dict(suits=["spade", "clover", "heart", "diamond", "star"],
                            number=[3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1, 2],
                            power=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
                            magic=[],
                            sp_cards=["joker"]
                            )

    def __init__(self,
                 client_number: int,
                 settings: dict = None,
                 ):
        if settings is None:
            self.settings = self.settings_DEFAULT
        else:
            self.settings = settings

        self.client_number = client_number
        self.cards: List[Card] = []
        self.players: List[List[Card]] = []

        for suit in self.settings["suits"]:
            for number, power in zip(self.settings["number"], self.settings["power"]):
                self.cards.append(Card(suit + number, int(power), []))
        for sp_card in self.settings["sp_cards"]:
            self.cards.append(Card(sp_card, 100, []))

    def game_init(self):
        pass

    def __register_users(self):
        return

    def __logging(self):
        pass
