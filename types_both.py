from enum import Enum


class UserDataType(Enum):
    Name = "name"


class UserStatusType(Enum):
    Updating = "updating"
    QueueIn = "queue_in"
    Lobby = "lobby"
    InGame = "in_game"


class GameOperationType(Enum):
    pull = "pull"
