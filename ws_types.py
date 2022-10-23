from enum import Enum
from ws_notify_model import *
from ws_request_model import *

RqTypes = {
    "GSU": RqGetStatusUser,
    "GSG": RqGetStatusGame,
    "CSU": RqChangeStatusUser,
    "OPE": RqOpePullCards
}
# NtTypes.playなどさらにjsonに階層がある場合は、parserをメソッドで追加して、クロージャーを返す
NtTypes = {
    "status": NtStatus,

}


class UserDataType(Enum):
    Name = "name"


class NtType(Enum):
    Status = "status"
    Profile = "profile"
    Play = "play"
    Game = "game"


class UserStatusType(Enum):
    Updating = "updating"
    QueueIn = "queue_in"
    Lobby = "lobby"
    InGame = "in_game"


class GameOperationType(Enum):
    pull = "pull"
    give = "give"


class RqType(Enum):
    GetStatusUser = "GSU"
    GetStatusGame = "GSG"
    ChangeStatusUser = "CSU"
    Operation = "OPE"
