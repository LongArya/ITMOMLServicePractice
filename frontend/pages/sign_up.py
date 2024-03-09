import dash
from dash import Dash, html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

dash.register_page(__name__)


@callback(
    [Output("hidden-signup-span", "children"), Input("signup-button", "n_clicks")]
)
def on_signup_button_click(n):
    print(f"\nCLICKED SIGN UP BUTTON {n}")
    return [""]


def get_signup_form():
    email_input = html.Div(
        [
            dbc.Input(type="email", id="example-email", placeholder="Enter email"),
        ],
        className="mb-3",
    )

    username_input = html.Div(
        [
            dbc.Input(type="text", id="username", placeholder="Enter username"),
        ],
        className="mb-3",
    )

    password_input = html.Div(
        [
            dbc.Input(
                type="password",
                id="example-password",
                placeholder="Enter password",
            ),
        ],
        className="mb-3",
    )
    signup_button = dbc.Button(
        "Sign Up", id="signup-button", color="primary", n_clicks=0
    )
    sign_up_form = dbc.Form(
        [email_input, username_input, password_input, signup_button],
        style={"margin-right": "5%", "margin-left": "5%"},
    )
    return sign_up_form


def layout():
    sign_up_form = get_signup_form()
    layout = html.Div(
        [
            html.H5("Sign Up", style={"margin-top": "5%", "margin-left": "5%"}),
            html.Div(children=[sign_up_form]),
            html.Span(id="hidden-signup-span", style={"display": "none"}),
        ]
    )
    return layout
