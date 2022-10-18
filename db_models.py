from datetime import datetime, timedelta

from passlib.context import CryptContext
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String, Date, DateTime, PickleType
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.dialects.postgresql import UUID, VARCHAR, DATE, TIMESTAMP
from sqlalchemy.sql.functions import current_timestamp
import ulid
from db_config import Base, SessionLocal, engine
from user import UserModel, UserCreate


class UserOrm(Base):
    @staticmethod
    def from_pymodel(pymodel: UserModel | UserCreate):
        pymodel.password = CryptContext(schemes=["bcrypt"], deprecated="auto").hash(pymodel.password)
        return UserOrm(**pymodel.dict())

    @staticmethod
    def set_expired_time():
        return datetime.now() + timedelta(days=8)

    __tablename__ = "users"
    # :TODO REFACTOR GENERIC TYPES to POSTGRES TYPES
    ulid = Column(UUID(as_uuid=True), primary_key=True, unique=True, default=ulid.new().uuid)
    name = Column(VARCHAR(255))
    password = Column(VARCHAR(1023))
    expired_time = Column(TIMESTAMP, nullable=True, default=set_expired_time())
    created_at = Column(TIMESTAMP, nullable=True, default=current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=True, default=current_timestamp())

# class BattleRecord(Base):
#     __tablename__ = "battle_records"
#     bd_id = Column(UUID, primary_key=True)
#     bd_record = Column(PickleType)
#     bd_time = Column(DateTime)
#     bd_p1 = Column(UUID, ForeignKey("users.ulid_"))
#     bd_p2 = Column(UUID, ForeignKey("users.ulid_"))
#     bd_p3 = Column(UUID, ForeignKey("users.ulid_"))
#     bd_p4 = Column(UUID, ForeignKey("users.ulid_"))
