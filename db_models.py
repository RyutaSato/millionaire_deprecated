from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.types import Integer, String, Date, DateTime, PickleType, ARRAY
from sqlalchemy.ext.declarative import declarative_base
import ulid
import db_config

Base = declarative_base()
SessionClass = sessionmaker(db_config.db_engine)


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, nullable=False, default=ulid.new().int)
    user_handle_name = Column(String(255))
    user_first_name = Column(String(255))
    user_last_name = Column(String(255))
    user_email = Column(String(255))
    user_birthday = Column(Date)
    created_on = Column(DateTime)
    updated_on = Column(DateTime)

    def print_user(self):
        return print(
            f"id:       {self.user_id}"
            f"uuid:     {self.user_uuid}"
            f"h_name:   {self.user_handle_name}"
            f"name:     {self.user_first_name} / {self.user_last_name}"
            f"mail:     {self.user_email}"
            f"birthday: {self.user_birthday}"
        )

class BattleRecord(Base):
    __tablename__ = "battle_records"
    bd_id = Column(Integer, primary_key=True)
    bd_record = Column(PickleType)
    bd_time = Column(DateTime)
    bd_p1 = Column(Integer, ForeignKey("users.user_id"))
    bd_p2 = Column(Integer, ForeignKey("users.user_id"))
    bd_p3 = Column(Integer, ForeignKey("users.user_id"))
    bd_p4 = Column(Integer, ForeignKey("users.user_id"))


Base.metadata.create_all(db_config.db_engine)
