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

if __name__ == "__main__":
    tmp1 = UserOrm(
        ulid=ulid.new().uuid,
        name="rsato",
        password="password",
        expired_time=datetime.now(),
        created_at=datetime.now(),
        updated_at=datetime.now()

    )
    tmp2 = UserPydanticModel.from_orm(tmp1)
    tmp3 = UserOrm(**tmp2.dict())
    tmp4 = UserPydanticModel.from_orm(tmp3)
    tmp5 = UserOrm.from_pymodel(tmp4)
    print(tmp4)
    print(tmp5.__dict__)
