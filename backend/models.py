from typing import Optional

from typing import List
from datetime import datetime
from sqlmodel import (
    Field,
    Relationship,
    SQLModel,
)


class Model(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    cost: int

    predictions: List["Prediction"] = Relationship(back_populates="model")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False

    predictions: List["Prediction"] = Relationship(back_populates="user_initiator")


class Prediction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_initiator_id: int = Field(foreign_key="user.id")

    model_id: int = Field(foreign_key="model.id")
    cost: int
    started_at: datetime
    finished_at: datetime
    predicted_value: bool

    model: Model = Relationship(back_populates="predictions")
    user_initiator: User = Relationship(back_populates="predictions")
