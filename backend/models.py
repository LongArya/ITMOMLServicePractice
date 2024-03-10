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
    balance: int

    predictions: List["Prediction"] = Relationship(back_populates="user_initiator")


class Prediction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    model_id: int = Field(foreign_key="model.id")
    rq_job_id: str
    rq_status: str
    cost: int
    started_at: datetime
    # prediction output
    result: Optional[str] = Field(default=None)
    # input fields
    Gender: str
    Age_at_diagnosis: int
    Primary_Diagnosis: str
    Race: str
    IDH1: str
    TP53: str
    ATRX: str
    PTEN: str
    EGFR: str
    CIC: str
    MUC16: str
    PIK3CA: str
    NF1: str
    PIK3R1: str
    FUBP1: str
    RB1: str
    NOTCH1: str
    BCOR: str
    CSMD3: str
    SMARCA4: str
    GRIN2A: str
    IDH2: str
    FAT4: str
    PDGFRA: str

    model: Model = Relationship(back_populates="predictions")
    user_initiator: User = Relationship(back_populates="predictions")
