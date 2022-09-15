# this is PLUGIN between database and ORM
# See https://fastapi.tiangolo.com/ja/tutorial/sql-databases/#crud-utils
from uuid import UUID

from sqlalchemy.orm import Session

from db_models import UserOrm


# Only Sample
def get_user(db: Session, uuid: UUID):
    return db.query(UserOrm).filter(UserOrm.ulid == uuid).first()


# Only Sample
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserOrm).offset(skip).limit(limit).all()


def add_user_to_db(db: Session, user: UserOrm):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def verify_name(db: Session, name: str) -> UserOrm:
    return db.query(UserOrm).filter(UserOrm.name == name).first()
