import dash
from http import HTTPStatus
from requests import Response
from datetime import date, datetime
from dash import Dash, html, dcc, Input, Output, callback, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from typing import List, Optional, Tuple, Dict
from frontend.utils import (
    get_difference_between_dates_in_days,
    datetime_from_YYYY_MM_DD,
)
from frontend.api_utils import (
    wait_untill_prediction_end,
    init_predict,
    generate_test_prediction_input,
    get_current_user_data_via_api,
)

REQUIRED_GENES = [
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
GENDER_MAPPING: Dict[str, str] = {"Male": "Male", "Female": "Female"}
RACE_MAPPING: Dict[str, str] = {
    "White": "white",
    "Black": "black or african american",
    "Asian": "asian",
}

dash.register_page(__name__)


def compose_model_input_from_user_input(
    selected_gender: str,
    selected_race: str,
    selected_diagnosis: str,
    selected_genes1: List[str],
    selected_genes2: List[str],
    selected_birthday: str,
    selected_diagnosis_data: str,
) -> Dict:

    birtday_date: datetime = datetime_from_YYYY_MM_DD(selected_birthday)
    diagnosis_date: datetime = datetime_from_YYYY_MM_DD(selected_diagnosis_data)
    diagnosis_age_days = get_difference_between_dates_in_days(
        start_date=birtday_date, end_date=diagnosis_date
    )
    model_input = {
        "Gender": GENDER_MAPPING[selected_gender],
        "Age_at_diagnosis": diagnosis_age_days,
        "Primary_Diagnosis": selected_diagnosis,
        "Race": RACE_MAPPING[selected_race],
    }

    selected_genes = []
    if selected_genes1 is not None:
        selected_genes += selected_genes1
    if selected_genes2 is not None:
        selected_genes + selected_genes2

    for gene in REQUIRED_GENES:
        if gene in selected_genes:
            model_input[gene] = "MUTATED"
        else:
            model_input[gene] = "NOT_MUTATED"
    return model_input


def update_state_after_model_prediction(
    model_name: str,
    selected_gender: Optional[str],
    selected_race: Optional[str],
    selected_diagnosis: Optional[str],
    selected_genes1: List[str],
    selected_genes2: List[str],
    selected_birthday: Optional[str],
    selected_diagnosis_data: Optional[str],
    session_data,
) -> Tuple[bool, bool, bool]:
    trigger_missing_data: bool = False
    trigger_prediction_end: bool = False
    trigger_not_enough_currency: bool = False

    if None in [
        selected_birthday,
        selected_gender,
        selected_race,
        selected_birthday,
        selected_diagnosis_data,
        selected_diagnosis,
    ]:
        trigger_missing_data = True
        return (
            session_data,
            trigger_missing_data,
            trigger_prediction_end,
            trigger_not_enough_currency,
        )

    model_input = compose_model_input_from_user_input(
        selected_gender=selected_gender,
        selected_race=selected_race,
        selected_diagnosis=selected_diagnosis,
        selected_genes1=selected_genes1,
        selected_genes2=selected_genes2,
        selected_birthday=selected_birthday,
        selected_diagnosis_data=selected_diagnosis_data,
    )
    start_pred_responce: Response = init_predict(
        prediction_data=model_input, token=session_data["token"], model_name=model_name
    )
    if start_pred_responce.status_code == HTTPStatus.PAYMENT_REQUIRED:
        trigger_not_enough_currency = True
        return (
            session_data,
            trigger_missing_data,
            trigger_prediction_end,
            trigger_not_enough_currency,
        )
    if start_pred_responce.status_code != HTTPStatus.OK:
        print(start_pred_responce.json())
        return (
            session_data,
            trigger_missing_data,
            trigger_prediction_end,
            trigger_not_enough_currency,
        )

    prediction_id = start_pred_responce.json()["id"]
    prediction_responce = wait_untill_prediction_end(
        prediction_id=prediction_id, token=session_data["token"]
    )
    if prediction_responce.status_code != HTTPStatus.OK:
        return (
            session_data,
            trigger_missing_data,
            trigger_prediction_end,
            trigger_not_enough_currency,
        )

    me = get_current_user_data_via_api(access_token=session_data["token"])
    session_data["current_user"] = me.json()
    trigger_prediction_end = True
    return (
        session_data,
        trigger_missing_data,
        trigger_prediction_end,
        trigger_not_enough_currency,
    )


@callback(
    Output("session", "data", allow_duplicate=True),
    Output("data-alert", "is_open", allow_duplicate=True),
    Output("ended_pred-alert", "is_open", allow_duplicate=True),
    Output("not_enough_currency-alert", "is_open", allow_duplicate=True),
    Input("logreg_button", "n_clicks"),
    State("gender-dropdown", "value"),
    State("race-dropdown", "value"),
    State("diagnosis-dropdown", "value"),
    State("genes_checklist1", "value"),
    State("genes_checklist2", "value"),
    State("birthday_picker", "date"),
    State("diagnosis_date_picker", "date"),
    State("session", "data"),
    prevent_initial_call=True,
)
def log_reg_callback(
    n_clicks: int,
    selected_gender: Optional[str],
    selected_race: Optional[str],
    selected_diagnosis: Optional[str],
    selected_genes1: List[str],
    selected_genes2: List[str],
    selected_birthday: Optional[str],
    selected_diagnosis_data: Optional[str],
    session_data,
) -> Tuple[List[Dict], bool, bool, bool]:
    if n_clicks is None:
        raise PreventUpdate
    if n_clicks > 0:
        return update_state_after_model_prediction(
            model_name="logreg",
            selected_gender=selected_gender,
            selected_race=selected_race,
            selected_diagnosis=selected_diagnosis,
            selected_genes1=selected_genes1,
            selected_genes2=selected_genes2,
            selected_birthday=selected_birthday,
            selected_diagnosis_data=selected_diagnosis_data,
            session_data=session_data,
        )


@callback(
    Output("dtree_button", "n_clicks"),
    Input("dtree_button", "n_clicks"),
    State("gender-dropdown", "value"),
    State("race-dropdown", "value"),
    State("diagnosis-dropdown", "value"),
    State("genes_checklist1", "value"),
    State("genes_checklist2", "value"),
    State("birthday_picker", "date"),
    State("diagnosis_date_picker", "date"),
    State("session", "data"),
)
def dtree_callback(
    n_clicks: int,
    selected_gender: Optional[str],
    selected_race: Optional[str],
    selected_diagnosis: Optional[str],
    selected_genes1: List[str],
    selected_genes2: List[str],
    selected_birthday: Optional[str],
    selected_diagnosis_data: Optional[str],
    session_data,
) -> Tuple[List[Dict], bool, bool, bool]:
    if n_clicks is None:
        raise PreventUpdate
    if n_clicks > 0:
        output = update_state_after_model_prediction(
            model_name="dtree",
            selected_gender=selected_gender,
            selected_race=selected_race,
            selected_diagnosis=selected_diagnosis,
            selected_genes1=selected_genes1,
            selected_genes2=selected_genes2,
            selected_birthday=selected_birthday,
            selected_diagnosis_data=selected_diagnosis_data,
            session_data=session_data,
        )
        return n_clicks + 1


@callback(
    Output("rand_forest_button", "n_clicks"),
    Input("rand_forest_button", "n_clicks"),
    State("gender-dropdown", "value"),
    State("race-dropdown", "value"),
    State("diagnosis-dropdown", "value"),
    State("genes_checklist1", "value"),
    State("genes_checklist2", "value"),
    State("birthday_picker", "date"),
    State("diagnosis_date_picker", "date"),
    State("session", "data"),
)
def random_forest_callback(
    n_clicks: int,
    selected_gender: Optional[str],
    selected_race: Optional[str],
    selected_diagnosis: Optional[str],
    selected_genes1: List[str],
    selected_genes2: List[str],
    selected_birthday: Optional[str],
    selected_diagnosis_data: Optional[str],
    session_data,
) -> Tuple[List[Dict], bool, bool, bool]:
    if n_clicks is None:
        raise PreventUpdate
    if n_clicks > 0:
        output = update_state_after_model_prediction(
            model_name="random-forest",
            selected_gender=selected_gender,
            selected_race=selected_race,
            selected_diagnosis=selected_diagnosis,
            selected_genes1=selected_genes1,
            selected_genes2=selected_genes2,
            selected_birthday=selected_birthday,
            selected_diagnosis_data=selected_diagnosis_data,
            session_data=session_data,
        )
        return n_clicks + 1


def create_model_cards():
    log_reg_card = dbc.Card(
        [
            dbc.CardHeader("Logistic Regression", style={"font-weight": "bolder"}),
            dbc.CardImg(src="assets/models_images/log_reg.jpg", top=True),
            dbc.CardBody(
                [
                    html.P("cost 100P", className="card-text"),
                ]
            ),
            dbc.CardFooter(dbc.Button("Predict", id="logreg_button")),
        ],
        style={"width": "18rem"},
    )

    dtree_card = dbc.Card(
        [
            dbc.CardHeader("Decision Tree", style={"font-weight": "bolder"}),
            dbc.CardImg(src="assets/models_images/dtree.jpg", top=True),
            dbc.CardBody(
                [
                    html.P("cost 200P", className="card-text"),
                ]
            ),
            dbc.CardFooter(dbc.Button("Predict", id="dtree_button")),
        ],
        style={"width": "18rem"},
    )

    rf_card = dbc.Card(
        [
            dbc.CardHeader("Random Forest", style={"font-weight": "bolder"}),
            dbc.CardImg(src="assets/models_images/random_forest.jpg", top=True),
            dbc.CardBody(
                [
                    html.P("cost 300P", className="card-text"),
                ]
            ),
            dbc.CardFooter(dbc.Button("Predict", id="rand_forest_button")),
        ],
        style={"width": "18rem"},
    )

    cards = dbc.Row(
        [
            dbc.Col(log_reg_card, width="auto"),
            dbc.Col(dtree_card, width="auto"),
            dbc.Col(rf_card, width="auto"),
        ],
        class_name="h-75",
        style={"margin-left": "2%", "margin-top": "2%"},
    )
    return cards


def create_checkboxes_for_genes() -> html.Div:
    genes_mutataion_checkboxes = dbc.Row(
        [
            dbc.Col(
                dcc.Checklist(
                    [
                        "IDH1",
                        "TP53",
                        "ATRX",
                        "PTEN",
                        "EGFR",
                        "CIC",
                        "MUC16",
                        "PIK3CA",
                        "NF1",
                    ],
                    id="genes_checklist1",
                )
            ),
            dbc.Col(
                dcc.Checklist(
                    [
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
                    ],
                    id="genes_checklist2",
                )
            ),
        ]
    )
    return genes_mutataion_checkboxes


def create_user_input_form() -> None:
    birthday_form = dbc.Row(
        [
            dbc.Col(dbc.Label("Date of birth")),
            dbc.Col(
                dcc.DatePickerSingle(
                    id="birthday_picker",
                )
            ),
        ]
    )
    diagnosis_date_form = dbc.Row(
        [
            dbc.Col(dbc.Label("Date of diagnosis")),
            dbc.Col(
                dcc.DatePickerSingle(
                    id="diagnosis_date_picker",
                )
            ),
        ]
    )
    gender_form = dbc.Row(
        [
            dbc.Col(dbc.Label("Gender")),
            dbc.Col(dcc.Dropdown(["Male", "Female"], id="gender-dropdown")),
        ]
    )
    race_form = dbc.Row(
        [
            dbc.Col(dbc.Label("Race")),
            dbc.Col(dcc.Dropdown(["White", "Black", "Asian"], id="race-dropdown")),
        ]
    )
    diagnosis_form = dbc.Row(
        [
            dbc.Col(dbc.Label("Diagnosis")),
            dbc.Col(
                dcc.Dropdown(
                    [
                        "Oligodendroglioma, NOS",
                        "Mixed glioma",
                        "Astrocytoma, NOS",
                        "Astrocytoma, anaplastic",
                        "Oligodendroglioma, anaplastic",
                        "Glioblastoma",
                    ],
                    id="diagnosis-dropdown",
                )
            ),
        ]
    )
    genes_checkboxes = create_checkboxes_for_genes()
    data_input_form = dbc.Form(
        [
            birthday_form,
            html.Hr(),
            diagnosis_date_form,
            html.Hr(),
            gender_form,
            html.Hr(),
            race_form,
            html.Hr(),
            diagnosis_form,
            html.Hr(),
            dbc.Label("Specify genes mutation"),
            genes_checkboxes,
        ],
        id="user_input_form",
        style={"margin-right": "5%", "margin-left": "5%"},
    )
    return data_input_form


def layout():
    input_form = create_user_input_form()
    cards = create_model_cards()
    layout = html.Div(
        [
            html.H1(
                "ML Classification models",
                style={"margin-left": "2%", "margin-top": "2%"},
            ),
            dbc.Alert(
                "Missing input data",
                color="warning",
                id="data-alert",
                is_open=False,
                duration=1000,
            ),
            dbc.Alert(
                "Prediction has ended",
                color="success",
                id="ended_pred-alert",
                is_open=False,
                duration=1000,
            ),
            dbc.Alert(
                "Not enough currency",
                color="danger",
                id="not_enough_currency-alert",
                is_open=False,
                duration=1000,
            ),
            dbc.Row([dbc.Col(cards), dbc.Col(input_form)]),
        ]
    )
    return layout
