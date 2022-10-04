from enum import Enum

from pydantic import BaseModel
from fast_api_project.player import Player
from fast_api_project.card import Card


class PlayerOperationEnum(Enum):
    skip = "skip"
    pull = "pull"
    give = "give"


class PlayerOperation(BaseModel):
    player: Player
    cards: list[Card] = []
    targets: list[Player] = []
    operation: PlayerOperationEnum = PlayerOperationEnum.pull

    class Config:
        use_enum_values = True
