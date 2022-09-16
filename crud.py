# this is PLUGIN between database and ORM
# See https://fastapi.tiangolo.com/ja/tutorial/sql-databases/#crud-utils
from uuid import UUID

from sqlalchemy.orm import Session

from db_models import UserOrm


def add_user_to_db(db: Session, user: UserOrm):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def verify_name(db: Session, name: str) -> UserOrm:
    return db.query(UserOrm).filter(UserOrm.name == name).first()
