from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from config import Config


class History(BaseModel):
    board_id: UUID
    created_at: datetime
    ended_at: datetime
    users: list[UUID]
    config: Config
