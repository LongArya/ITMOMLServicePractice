import re
import pandas as pd
from typing import Optional, Tuple

AGE_AT_DIAGNOSIS_FULL_PATTERN = r"(?P<years>[0-9]*) years (?P<days>[0-9]*) days"
AGE_AT_DIAGNOSIS_SHORT_PATTERN = r"(?P<years>[0-9]*) years"
DAYS_IN_YEAR = 365
RANDOM_SEED = 15

TARGET_VALUE_COLUMN = "Grade"
CATEGORICAL_COLUMN = ["Gender", "Primary_Diagnosis", "Race"]
GENES_COLUMNS = [
    "IDH1",
    "TP53",
    "ATRX",
    "PTEN",
    "EGFR",
    "CIC",
    "MUC16",
    "PIK3CA",
    "NF1",
    "PIK3R1",
    "FUBP1",
    "RB1",
    "NOTCH1",
    "BCOR",
    "CSMD3",
    "SMARCA4",
    "GRIN2A",
    "IDH2",
    "FAT4",
    "PDGFRA",
]
TRAIN_COLUMNS = [
    "Gender",
    "Age_at_diagnosis",
    "Primary_Diagnosis",
    "Race",
] + GENES_COLUMNS


# BASIC PREPROCESSING
def parse_age_with_full_pattern(age_string: str) -> Optional[int]:
    match = re.match(AGE_AT_DIAGNOSIS_FULL_PATTERN, age_string)
    if match is None:
        return None
    match = match.groupdict()
    years = int(match["years"])
    days = int(match["days"])
    return years * DAYS_IN_YEAR + days


def parse_age_with_short_pattern(age_string: str) -> Optional[int]:
    match = re.match(AGE_AT_DIAGNOSIS_SHORT_PATTERN, age_string)
    if match is None:
        return None

    match = match.groupdict()
    years = int(match["years"])
    return years * DAYS_IN_YEAR


def parse_age_string_as_number_of_days(age_string: str) -> Optional[int]:
    output: Optional[int] = parse_age_with_full_pattern(age_string)
    if output is None:
        output = parse_age_with_short_pattern(age_string)
    if output is None:
        raise ValueError(f"could not parse {age_string}")
    return output


def preprocess_data(data: pd.DataFrame) -> pd.DataFrame:
    preprocessed_data = data.copy()
    preprocessed_data = preprocessed_data.drop(columns=["Project", "Case_ID"])
    preprocessed_data = preprocessed_data[preprocessed_data["Race"] != "not reported"]
    preprocessed_data = preprocessed_data[preprocessed_data["Age_at_diagnosis"] != "--"]
    preprocessed_data["Age_at_diagnosis"] = preprocessed_data["Age_at_diagnosis"].apply(
        parse_age_string_as_number_of_days
    )
    # drop race that is present only once
    preprocessed_data = preprocessed_data[
        preprocessed_data["Race"] != "american indian or alaska native"
    ]
    return preprocessed_data


# ENCODING
def get_X_y_split(data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    x = data.drop(columns=[TARGET_VALUE_COLUMN])
    y = data[TARGET_VALUE_COLUMN]
    return x, y


def encode_gene_mutation(gene_mutation: str) -> float:
    assert gene_mutation in ["MUTATED", "NOT_MUTATED"]
    mutated = gene_mutation == "MUTATED"
    return float(mutated)


def encode_grade(grade: str) -> float:
    assert grade in ["LGG", "GBM"]
    gbm = grade == "GBM"
    return float(gbm)


def encode_data(
    data: pd.DataFrame, target_value_is_expected: bool = True
) -> pd.DataFrame:
    encoded_data = data.copy()
    categorical_data = data[CATEGORICAL_COLUMN]
    encoded_categorical_data = pd.get_dummies(
        categorical_data, drop_first=True, dtype=float
    )
    encoded_data[GENES_COLUMNS] = encoded_data[GENES_COLUMNS].map(encode_gene_mutation)
    if target_value_is_expected:
        encoded_data[TARGET_VALUE_COLUMN] = encoded_data[TARGET_VALUE_COLUMN].map(
            encode_grade
        )
    encoded_data = encoded_data.drop(columns=CATEGORICAL_COLUMN)
    encoded_data = pd.concat((encoded_data, encoded_categorical_data), axis=1)
    return encoded_data


def get_single_row_table() -> pd.DataFrame:
    data = ["Male", 100, "Oligodendroglioma, NOS", "white"] + ["MUTATED"] * 20
    single_row_table = pd.DataFrame([data], columns=TRAIN_COLUMNS)
    return single_row_table
