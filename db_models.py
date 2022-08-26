from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String, Date, DateTime, PickleType
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, VARCHAR
import ulid
from db_config import Base, SessionLocal, engine


class User(Base):
    __tablename__ = "users"
    # :TODO REFACTOR FROM GENERIC TYPES to POSTGRES TYPES
    uuid = Column(UUID, primary_key=True, nullable=False, default=ulid.new())
    user_handle_name = Column(String(255))
    user_first_name = Column(String(255))
    user_last_name = Column(String(255))
    user_email = Column(String(255))
    user_birthday = Column(Date)
    created_on = Column(DateTime)
    updated_on = Column(DateTime)

    def print_user(self):
        return print(
            f"id:       {self.uuid}"
            f"uuid:     {self.user_uuid}"
            f"h_name:   {self.user_handle_name}"
            f"name:     {self.user_first_name} / {self.user_last_name}"
            f"mail:     {self.user_email}"
            f"birthday: {self.user_birthday}"
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
