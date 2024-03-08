from typing import Optional
from pprint import pprint
from typing import List
from datetime import datetime
from sqlmodel import (
    Field,
    Relationship,
    Session,
    SQLModel,
    create_engine,
    DateTime,
    select,
)
from pydantic import EmailStr
from backend.schemas.user import UserCreateSchema
from backend.models import User


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def add_rows_to_table(session: Session, rows: List[SQLModel]) -> None:
    for row in rows:
        session.add(row)
    session.commit()


def fill_table():

    session = Session(engine)
    users = [
        User(name="User1", email="user1@gmail.com"),
        User(name="User2", email="user2@gmail.com"),
    ]
    models = [Model(name="kNN", cost=20), Model(name="LogReg", cost=20)]
    add_rows_to_table(session, users)
    add_rows_to_table(session, models)

    session.close()


def add_predictions() -> None:
    session = Session(engine)
    now = datetime.now()
    preds = [
        Prediction(
            user_initiator_id=1, model_id=1, cost=25, started_at=now, finished_at=now
        )
    ]
    add_rows_to_table(session, preds)
    session.close()


def read_predictions() -> None:
    session = Session(engine)
    selector = select(Prediction)
    predictions = session.exec(selector)
    print("PREDICTIONS")
    for p in predictions:
        print("p.started_at")
        print(p.started_at)


def main():
    create_db_and_tables()
    # fill_table()
    # add_predictions()
    read_predictions()


if __name__ == "__main__":
    user_schema = UserCreateSchema(name="A", email="name@address.com", password="dfsdf")
    # pprint(user_schema)
    user = User.model_validate(user_schema, update={"hashed_password": "dd"})
    pprint(user)
