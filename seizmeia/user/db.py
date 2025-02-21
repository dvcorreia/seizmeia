from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

from seizmeia.db import Base
from seizmeia.user import schemas


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, index=True)


def get_user(db: Session, user_id: int) -> schemas.User | None:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None

    return schemas.User.from_orm(user)


def get_user_by_username(db: Session, username: str) -> schemas.User | None:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None

    return schemas.User.from_orm(user)


def get_users(
    db: Session, skip: int = 0, limit: int = 100
) -> list[schemas.User]:
    users = db.query(User).offset(skip).limit(limit).all()
    return [schemas.User.from_orm(user) for user in users]


def create_user(db: Session, user: schemas.UserCreate) -> schemas.User:
    db_user = User(
        username=user.username, email=user.email, password=user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return schemas.User.from_orm(db_user)


def get_user_password(db: Session, username: str) -> str | None:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None

    return user.password
