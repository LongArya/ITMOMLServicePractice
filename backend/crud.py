from typing import Any, Optional

from sqlmodel import Session, select

from backend.core.security import get_password_hash, verify_password
from backend.schemas.user import UserCreateSchema
from backend.models import User, Model
from backend.core.config import settings


def create_user(session: Session, user_create: UserCreateSchema) -> User:
    db_obj = User.model_validate(
        user_create,
        update={
            "hashed_password": get_password_hash(user_create.password),
            "balance": settings.USER_START_BALANCE,
        },
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def get_model_by_name(session: Session, model_name: str) -> Optional[Model]:
    statement = select(Model).where(Model.name == model_name)
    session_model = session.exec(statement).first()
    return session_model


def authenticate(session: Session, email: str, password: str) -> Optional[User]:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user
