from enum import Enum
from ws_notify_model import *

# keyは"nt_type"
NtTypes = {
    "status": NtStatus,
    "profile": NtProfile,
    # "play"は条件分岐
}

# keyは"pl_type"
NtPlayTypes = {
    "pull": NtPlayPullCards,
}


class NtType(Enum):
    Status = "status"
    Profile = "profile"
    Play = "play"
    Game = "game"
