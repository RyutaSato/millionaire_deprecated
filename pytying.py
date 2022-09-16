from datetime import datetime

from pydantic import BaseModel
from sqlalchemy.schema import Column
import ulid

from db_models import UserOrm
from uuid import UUID

class UserPydanticModel(BaseModel):
    ulid: UUID
    name: str
    password: str
    expired_time: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta
class Token(BaseModel):
    token: str
    token_type: str

def create_access_token(ulid: str, expire:datetime = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)):
    return jwt.encode({"sub": ulid, "exp": expire}, SECRET_KEY)

if __name__ == "__main__":
    print(create_access_token(ulid.new().str))