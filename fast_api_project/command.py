from enum import Enum

from pydantic import BaseModel
from fast_api_project.player import Player
from fast_api_project.card import Card


class OperationEnum(Enum):
    skip = 0
    pull = 1
    give = 2


class Command(BaseModel):
    player: Player
    cards: list[Card] = []
    targets: list[Player] = []
    operation: OperationEnum = OperationEnum.pull
