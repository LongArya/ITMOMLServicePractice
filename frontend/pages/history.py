from http import HTTPStatus
import dash
from http import HTTPStatus
from requests import Response
from dash import Dash, html, dcc, Input, Output, callback, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from typing import List, Dict, Tuple
from pprint import pprint
from frontend.api_utils import get_current_user_predictions_via_api


dash.register_page(__name__)


@callback(Output("user_history", "children"), Input("session", "data"))
def login_user(session_data: Dict) -> List:
    if "token" not in session_data:
        return []
    response = get_current_user_predictions_via_api(session_data["token"])
    if response.status_code != HTTPStatus.OK:
        return []
    preds = response.json()
    history_items = []
    for index, pred in enumerate(preds):
        print(index, pred)
        history_items.append(html.P(f"{pred['started_at']} : {pred['result']}"))
        if index != len(preds) - 1:
            history_items.append(html.Hr())
    return history_items


def layout():
    layout = html.Div(
        [
            html.H5("History", style={"margin-top": "5%", "margin-left": "5%"}),
            html.Div(
                children=[],
                id="user_history",
                style={"margin-right": "5%", "margin-left": "5%"},
            ),
        ]
    )
    return layout
