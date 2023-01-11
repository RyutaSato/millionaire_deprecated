import asyncio
import sys
from contextvars import Context
from datetime import datetime
from enum import Enum
from uuid import UUID
from pydantic import BaseModel
from fast_api_project.card import Card, CardNumber, CardSuite
import ulid


async def s(time: float = 1):
    await asyncio.sleep(time * 0.5)


class User(BaseModel):
    name: str
    id: int


class SampleModel(User):
    uuid: UUID
    created_at: datetime = datetime.now()
    friends: list[User] = []


class SampleModel2(User):
    created_at: datetime


sample = SampleModel(
    name="rsato",
    id=123,
    uuid=ulid.new().uuid,
    created_at=datetime.now(),
    friends=[User(id=111, name="aaa"), User(id=222, name="bbb")]
)


# admit_models = AdmittedModelsIn()
# admit_models
def dict_practice():
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


def pattern_practice():
    import re

    pattern1 = r"^(jo|sp|cl|di|he)(0|1|2|3|4|5|6|7|8|9|11|12|13)$"
    pattern = re.compile(pattern1)
    print(pattern)
    li = ["jo", "jo1", "jo24", "ja11", "cll11", "he00", "di01"]
    for i in li:
        literal = pattern.match(i)
        print(i, literal)
        if literal:
            literal = literal.groups()
            card = Card(suite=CardSuite(literal[0]),
                        number=CardNumber(int(literal[1])),
                        _strength=Card.set_strength(int(literal[1]))
                        )
            print(card.json())

    class TmpEnum(Enum):
        aaa = "aaa"
        bbb = "bbb"
        ccc = "ccc"

    string = '{"name": "aaa", "id": 123}'
    user = User.parse_raw(string)
    # pydantic.error_wrappers.ValidationError
    dct = {"aaa": "aaa"}
    for key in dict(user).keys():
        print(key)
    print()
    for key in TmpEnum.__dict__.keys():
        try:
            print(dct[str(key)])
        except KeyError as e:
            print(e.args)


async def task(i: int):
    print(f"task{i} start")
    try:
        await s(i)
    except asyncio.exceptions.CancelledError as e:
        print("task is cancelled")
    print(f"task{i} done")


def game(callback: asyncio.Task):
    print(f"callback is {callback.result()}")
    print("game is started")
    print("game is end")


async def future_practice():
    loop = asyncio.get_running_loop()
    future = loop.create_future()
    task_ = loop.create_task(task(2))
    # task_.cancel()
    print(task_.done())
    await s(1)
    task_.add_done_callback(game)
    task_.cancel()
    print(f"task is {task_.done()}")
    await s(5)


async def deco(func):
    print("this is deco start")
    await asyncio.sleep(5)

    def _deco(*args, **kwargs):
        print("this is _deco start")
        print(f"func value is {func(*args, **kwargs)}")
        print("this is _deco end")

    print("this is deco end")
    return _deco


#
# @deco
# def cul():
#     print("this is cul")
#     return 2

class DecoClass:
    @classmethod
    def create_class(cls):
        print("created class")
        return cls

    @deco
    def __init__(self):
        print("initialized!")

    print("aaa")

    @deco
    def aaa(self):
        return "aaa"


if __name__ == "__main__":
    _, q = map(int, input().split())
    for _ in range(q):
        t, a, b = map(int, input().split())
