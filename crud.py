# this is PLUGIN between database and ORM
# See https://fastapi.tiangolo.com/ja/tutorial/sql-databases/#crud-utils
from uuid import UUID

from sqlalchemy.orm import Session

from db_models import User
from response import LoginResponseModel
from user_base import authenticate_user

# Only Sample
def get_user(db: Session, uuid: UUID):
    return db.query(User).filter(User.ulid == uuid).first()

# Only Sample
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def resister_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)


def login_process(db: Session, name: str, law_password: str):
    result = db.query(User).filter(User.name == name).first()
    if result is not None and authenticate_user(law_password, result.password):
        return result
    return

