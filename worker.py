from pydantic import FilePath
from typing import Any
import pandas as pd
import pickle
from backend.schemas.prediction import (
    GliomaClassifierInput,
    Grade,
    Gender,
    PrimaryDiagnosis,
    Race,
)
from typing import Dict, Protocol, Optional
from ML_research.data_preprocessing import encode_data, get_single_row_table


class MlModel(Protocol):
    def predict():
        pass


def read_pickle(path: FilePath) -> Any:
    with open(path, "rb") as f:
        pickle_content = pickle.load(f)
    return pickle_content


ModelRegistry: Dict[str, MlModel] = {
    "logreg": read_pickle("ML_research/models/log_reg.pkl"),
    "dtree": read_pickle("ML_research/models/dtree.pkl"),
    "random-forest": read_pickle("ML_research/models/random_forest.pkl"),
}


def get_diverse_table_for_correct_dummy_enc() -> None:
    tables = []
    table = get_single_row_table()
    for gender in Gender:
        table_copy = table.copy()
        table_copy["Gender"] = gender.value
        tables.append(table_copy)
    for diagnosis in PrimaryDiagnosis:
        table_copy = table.copy()
        table_copy["Primary_Diagnosis"] = diagnosis.value
        tables.append(table_copy)
    for race in Race:
        table_copy = table.copy()
        table_copy["Race"] = race.value
        tables.append(table_copy)
    diverse_table = pd.concat(tables)
    return diverse_table


def convert_glioma_input_to_dframe(glioma_input: GliomaClassifierInput) -> pd.DataFrame:
    dump = glioma_input.model_dump()
    for k in dump.keys():
        v = dump[k]
        dump[k] = [v]
    frame = pd.DataFrame.from_dict(dump)
    return frame


def predict(model: MlModel, glioma_input: GliomaClassifierInput) -> Grade:
    diverse_table = get_diverse_table_for_correct_dummy_enc()
    pred_target = convert_glioma_input_to_dframe(glioma_input)
    encoder_input = pd.concat((pred_target, diverse_table))
    encoded_data = encode_data(encoder_input, target_value_is_expected=False)
    encoded_pred_target = encoded_data.iloc[[0], :]
    prediction = model.predict(encoded_pred_target)[0]
    grade = Grade.GBM if prediction else Grade.LGG
    return grade


def worker_function(model_name: str, glioma_input: GliomaClassifierInput) -> Grade:
    model: Optional[MlModel] = ModelRegistry.get(model_name, None)
    if model is None:
        raise ValueError(
            f"Model name {model_name} not one of {list(ModelRegistry.keys())}"
        )
    output: Grade = predict(model, glioma_input)
    return output
