from enum import Enum

from ws_request_model import *

RqTypes = {
    "GSU": RqGetStatusUser,
    "GSG": RqGetStatusGame,
    "CSU": RqChangeStatusUser,
    "OPE": RqOperation
}

OpeTypes = {
    "pull", RqOpePullCards
}


# NtTypes.playなどさらにjsonに階層がある場合は、parserをメソッドで追加して、クロージャーを返す


class RqType(Enum):
    GetStatusUser = "GSU"
    GetStatusGame = "GSG"
    ChangeStatusUser = "CSU"
    Operation = "OPE"
