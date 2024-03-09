import dash
from dash import Dash, html, dcc, Input, Output, callback, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from pprint import pprint

dash.register_page(__name__)


@callback(
    [
        Output("session", "data"),
        Input("login_button", "n_clicks"),
        State("session", "data"),
    ]
)
def on_login_button_click(n_clicks, data):
    if n_clicks is None:
        raise PreventUpdate
    if data is None:
        data = {"token": ""}
    if n_clicks > 0:
        print("set token")
        data["token"] = "alskdjflaksdj"
        print(data)
    pprint(f"nclicks: {n_clicks}, DATA AFTER LOGIN {data}")
    return [data]


def get_login_form():
    form = dbc.Form(
        dbc.Row(
            [
                dbc.Label("Email", width="auto"),
                dbc.Col(
                    dbc.Input(type="email", placeholder="Enter email"),
                    className="me-3",
                ),
                dbc.Label("Password", width="auto"),
                dbc.Col(
                    dbc.Input(type="password", placeholder="Enter password"),
                    className="me-3",
                ),
                dbc.Col(
                    dbc.Button("Login", id="login_button", color="primary", n_clicks=0),
                    width="auto",
                ),
            ],
            className="g-2",
        )
    )
    return form


def layout():
    form = get_login_form()
    layout = html.Div(
        [
            html.H5("Login", style={"margin-top": "5%", "margin-left": "5%"}),
            html.Div(
                children=[form], style={"margin-right": "5%", "margin-left": "5%"}
            ),
        ]
    )
    return layout
