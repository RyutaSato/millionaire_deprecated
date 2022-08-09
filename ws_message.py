from json import JSONEncoder, JSONDecoder, JSONDecodeError
from typing import Any
from datetime import datetime
from pydantic import BaseModel


class ResponseBaseModel(BaseModel):
    _client: str
    version: str
    datetime: datetime


    def __init__(self, msg: str, **data: Any):
        super().__init__(**data)
        json_decode = JSONDecoder()
        json_decode.decode(msg)
