import sys
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
import ulid

# class FriendModel(BaseModel):
#     id: int
#     name: str
#
#
# class SampleModel(BaseModel):
#     name: str
#     id: int
#     uuid: UUID
#     created_at: datetime
#     friends: list[FriendModel]

import asyncio

# sample = SampleModel(
#     name="rsato",
#     id=123,
#     uuid=ulid.new().uuid,
#     created_at=datetime.now(),
#     friends=[FriendModel(id=111, name="aaa"), FriendModel(id=222, name="bbb")]
# )
# json_str: str = sample.json()
# sample_from_str = SampleModel.parse_raw(json_str)
# print(sample_from_str)
