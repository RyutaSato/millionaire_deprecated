from pydantic import BaseModel
from datetime import datetime, timedelta
from uuid import UUID
import ulid


class WebSocketIn(BaseModel):
    sent_at: datetime

    def ping(self) -> timedelta:
        return datetime.now() - self.sent_at


class WebSocketOut(BaseModel):
    # WebSocket sending Model inherits this class
    obj_id: UUID = ulid.new().uuid
    sent_at: datetime
    type: str

