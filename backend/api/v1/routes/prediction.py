from typing import Any

from fastapi import APIRouter
from sqlmodel import delete, func, select
from backend.api.v1.dependencies import (
    SessionDep,
)
from pydantic import BaseModel, ConfigDict
from enum import Enum, auto


class GeneState(str, Enum):
    MUTATED = "MUTATED"
    NOT_MUTATED = "NOT_MUTATED"


class GliomaClassifierInput(BaseModel):
    IDH1: GeneState


router = APIRouter()


@router.post("/")
def test_pred(session: SessionDep, input: GliomaClassifierInput) -> Any:
    """
    Retrieve users.
    """
    a = input
    return input
