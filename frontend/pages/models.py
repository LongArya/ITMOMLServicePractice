import dash
from datetime import date, datetime
from dash import Dash, html, dcc, Input, Output, callback, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from typing import List, Optional, Tuple, Dict
from frontend.utils import (
    get_difference_between_dates_in_days,
    datetime_from_YYYY_MM_DD,
)

dash.register_page(__name__)


# get model by name
def call_model_predict_by_name(access_token: str, model_name: str):
    pass


@callback(
    [
        Output("session", "data", allow_duplicate=True),
        Output("data-alert", "is_open"),
        Output("started_pred-alert", "is_open"),
        Output("not_enough_currency-alert", "is_open"),
        Input("logreg_button", "n_clicks"),
        State("gender-dropdown", "value"),
        State("race-dropdown", "value"),
        State("genes_checklist1", "value"),
        State("genes_checklist2", "value"),
        State("birthday_picker", "date"),
        State("diagnosis_date_picker", "date"),
        State("session", "data"),
    ],
    prevent_initial_call=True,
)
def log_reg_callback(
    n_clicks: int,
    selected_gender: Optional[str],
    selected_race: Optional[str],
    selected_genes1: List[str],
    selected_genes2: List[str],
    selected_birthday: Optional[str],
    selected_diagnosis_data: Optional[str],
    data,
) -> Tuple[List[Dict], bool, bool, bool]:
    trigger_missing_data: bool = False
    trigger_prediction_start: bool = False
    trigger_not_enough_currency: bool = False

    if n_clicks is None:
        raise PreventUpdate
    if n_clicks > 0:
        print("clickled on logreg model")
    print(f"selected gender = {selected_gender}")
    print(f"Data = {data}")
    if None in [
        selected_birthday,
        selected_gender,
        selected_race,
        selected_birthday,
        selected_diagnosis_data,
    ]:
        trigger_missing_data = True
    else:
        pass
        trigger_prediction_start = True
        birtday_date: datetime = datetime_from_YYYY_MM_DD(selected_birthday)
        diagnosis_date: datetime = datetime_from_YYYY_MM_DD(selected_diagnosis_data)
        diagnosis_age_days = get_difference_between_dates_in_days(
            start_date=birtday_date, end_date=diagnosis_date
        )
        print(f"diagnosis age days = {diagnosis_age_days}")
    return (
        data,
        trigger_missing_data,
        trigger_prediction_start,
        trigger_not_enough_currency,
    )


def create_model_cards():
    log_reg_card = dbc.Card(
        [
            dbc.CardHeader("Logistic Regression", style={"font-weight": "bolder"}),
            dbc.CardImg(src="assets/models_images/log_reg.jpg", top=True),
            dbc.CardBody(
                [
                    html.P("cost 10P", className="card-text"),
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
                    html.P("cost 10P", className="card-text"),
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
                    html.P("cost 10P", className="card-text"),
                ]
            ),
            dbc.CardFooter(dbc.Button("Predict")),
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
                "Started prediction",
                color="success",
                id="started_pred-alert",
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
