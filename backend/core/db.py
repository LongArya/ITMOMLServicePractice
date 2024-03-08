from backend.models import User, Prediction, Model
from backend.core.config import settings
from sqlmodel import create_engine, SQLModel


engine = create_engine(str(settings.SQLALCHEMY_SQLITE_DATABASE_URI))


def init_db():
    SQLModel.metadata.create_all(engine)
