import sys
from datetime import datetime
from enum import Enum
from uuid import UUID
from pydantic import BaseModel
import ulid


class FriendModel(BaseModel):
    id: int
    name: str


class User(BaseModel):
    name: str
    id: int


class SampleModel(User):
    uuid: UUID
    created_at: datetime
    friends: list[FriendModel] = []


sample = SampleModel(
    name="rsato",
    id=123,
    uuid=ulid.new().uuid,
    created_at=datetime.now(),
    friends=[FriendModel(id=111, name="aaa"), FriendModel(id=222, name="bbb")]
)
tmp_dict = {}
tmp_dict["name"] = "rsato"
tmp_dict["id"] = 123
tmp_dict["uuid"] = ulid.new().uuid
tmp_dict["created_at"] = datetime.now()
json_str: str = sample.json()
sample_from_str = SampleModel.parse_raw(json_str)
sample_from_dict = SampleModel(**tmp_dict)
print(sample_from_dict.json())
print(sample_from_str)


class TmpEnum(Enum):
    aaa = "aaa"
    bbb = "bbb"
    ccc = "ccc"


print(TmpEnum("aaa"))
from ws_model_in import WebSocketIn, SelectedLobbyCommandIn, LobbyCommandEnum
