from enum import Enum
from ws_notify_model import *

# keyは"pl_type"
NtPlayTypes = {
    "pull": NtPlayPullCards,
    "my_turn": NtPlayMyTurn,
    "end": NtPlayEnd
}


class UserDataType(Enum):
    Name = "name"


class UserStatusType(Enum):
    Updating = "updating"
    QueueIn = "queue_in"
    Lobby = "lobby"
    InGame = "in_game"


class PlayOperationType(Enum):
    Pull = "pull"
    MyTurn = "my_turn"
    End = "end"
