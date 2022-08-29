from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String, Date, DateTime, PickleType
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.dialects.postgresql import UUID, VARCHAR, DATE, TIMESTAMP
from sqlalchemy.sql.functions import current_timestamp
import ulid
from db_config import Base, SessionLocal, engine


class User(Base):
    __tablename__ = "users"
    # :TODO REFACTOR GENERIC TYPES to POSTGRES TYPES
    ulid = Column(UUID, primary_key=True, unique=True, default=ulid.new().uuid)
    name = Column(VARCHAR(255))
    password = Column(VARCHAR(255))
    created_on = Column(TIMESTAMP, nullable=True, server_default=current_timestamp())
    updated_on = Column(TIMESTAMP, nullable=True, server_default=current_timestamp())

    def print_user(self):
        return print(
            f"id:       {self.uuid}"
            f"name:     {self.name}"
        )


class BattleRecord(Base):
    __tablename__ = "battle_records"
    bd_id = Column(UUID, primary_key=True)
    bd_record = Column(PickleType)
    bd_time = Column(DateTime)
    bd_p1 = Column(UUID, ForeignKey("users.uuid"))
    bd_p2 = Column(UUID, ForeignKey("users.uuid"))
    bd_p3 = Column(UUID, ForeignKey("users.uuid"))
    bd_p4 = Column(UUID, ForeignKey("users.uuid"))


# :TODO この関数は main.py の app = FastAPI()手前に移動予定
Base.metadata.create_all(engine)
