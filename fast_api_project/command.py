from enum import Enum

from pydantic import BaseModel
from player import Player
from card import Card

class OperationEnum(Enum):
    skip = 0
    pull = 1
    give = 2


class Command(BaseModel):
    player: Player
    cards: list[Card] = []
    targets: list[Player] = []
    operation: OperationEnum = OperationEnum.pull

