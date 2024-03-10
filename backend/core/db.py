from backend.models import User, Prediction, Model
from backend.core.config import settings
from sqlmodel import create_engine, SQLModel, Session, select
from backend.crud import get_model_by_name


engine = create_engine(str(settings.SQLALCHEMY_SQLITE_DATABASE_URI))


def init_models():
    log_reg_model = Model(name="LogReg", cost=100)
    dtree = Model(name="Dtree", cost=200)
    random_forest = Model(name="RandomForest", cost=300)

    with Session(engine) as session:
        for model in [log_reg_model, dtree, random_forest]:
            existing_model = get_model_by_name(session=session, model_name=model.name)
            print(f"existing_model = {existing_model}")
            if existing_model is None:
                session.add(model)
                session.commit()
            else:
                print("skip adding models")


def init_db():
    SQLModel.metadata.create_all(engine)
    init_models()
