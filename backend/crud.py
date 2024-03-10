from typing import Any, Optional
import datetime
from sqlmodel import Session, select
from backend.core.security import get_password_hash, verify_password
from backend.schemas.user import UserCreateSchema
from backend.schemas.prediction import PredictionCreateSchema
from backend.models import User, Model, Prediction
from backend.core.config import settings

RQ_JOB_FINISHED_STATUS = "finished"
RQ_JOB_FAILED_STATUS = "failed"


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


def make_payment_for_user(session: Session, user_id: int, payment: int) -> None:
    db_obj = session.get(User, user_id)
    reduced_balance = db_obj.balance - payment
    if reduced_balance < 0:
        raise ValueError("Tried to commit payment without enough credits")
    db_obj.balance = reduced_balance
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)


def return_payment_to_user(session: Session, user_id: int, payment: int) -> None:
    db_obj = session.get(User, user_id)
    updated_balance = db_obj.balance + payment
    db_obj.balance = updated_balance
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)


def create_prediction_item(
    session: Session,
    model_id: int,
    user_id: int,
    rq_job_id: str,
    rq_status: str,
    prediction_input: PredictionCreateSchema,
) -> Prediction:
    inferred_model: Model = session.get(Model, model_id)
    current_timestamp: datetime.datetime = datetime.datetime.now()
    db_obj = Prediction.model_validate(
        prediction_input,
        update={
            "model_id": model_id,
            "user_id": user_id,
            "started_at": current_timestamp,
            "cost": inferred_model.cost,
            "rq_job_id": rq_job_id,
            "rq_status": rq_status,
        },
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_prediction_after_successfull_finish(
    session: Session, prediction_id: int, result: str
) -> Prediction:
    db_prediction: Prediction = session.get(Prediction, prediction_id)
    if db_prediction.rq_status == RQ_JOB_FINISHED_STATUS:
        return db_prediction

    db_prediction.rq_status = RQ_JOB_FINISHED_STATUS
    db_prediction.result = result
    session.add(db_prediction)
    session.commit()
    session.refresh(db_prediction)
    return db_prediction


def update_prediction_after_fail(session: Session, prediction_id: int) -> None:
    db_prediction: Prediction = session.get(Prediction, prediction_id)
    if db_prediction.rq_status == RQ_JOB_FINISHED_STATUS:
        return db_prediction

    db_prediction.rq_status = RQ_JOB_FAILED_STATUS
    session.add(db_prediction)
    session.commit()
    session.refresh(db_prediction)
    return_payment_to_user(
        session=session, user_id=db_prediction.user_id, payment=db_prediction.cost
    )
    return db_prediction


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
