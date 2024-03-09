import dash
from dash import Dash, dcc, html, Input, Output, callback, State
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc
import plotly.express as px
from pprint import pprint
from typing import List

load_figure_template("LUX")

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.LUX])


@callback(Output("app-navbar", "children"), Input("session", "data"))
def set_navbar(data):
    items = auth_only_navbar()
    print(f"set navbar based on {data}")
    if data.get("token", "") != "":
        items = all_items_navbar()
    return items


def get_auth_navbar_items() -> List[dbc.NavItem]:
    login_page = dash.page_registry["pages.login"]
    sign_up_page = dash.page_registry["pages.sign_up"]
    login_item = dbc.NavItem(dbc.NavLink("Login", href=login_page["relative_path"]))
    sign_up_item = dbc.NavItem(
        dbc.NavLink("Sign up", href=sign_up_page["relative_path"])
    )
    return [login_item, sign_up_item]


def get_authorized_navbar_dropdown_menu() -> dbc.DropdownMenu:
    dropdown = dbc.DropdownMenu(
        children=[
            dbc.DropdownMenuItem("Home", header=True),
            dbc.DropdownMenuItem("masyunya", href="#"),
            dbc.DropdownMenuItem("sima", href="#"),
        ],
        nav=True,
        in_navbar=True,
        label="More",
    )
    return dropdown


def auth_only_navbar() -> List:
    auth_navbar_items = get_auth_navbar_items()
    return auth_navbar_items


def all_items_navbar() -> List:
    all_navbar_items = get_auth_navbar_items()
    drodown_items = get_authorized_navbar_dropdown_menu()
    all_navbar_items.append(drodown_items)
    return all_navbar_items


def create_navbar():
    navbar_items = auth_only_navbar()
    navbar = dbc.NavbarSimple(
        id="app-navbar",
        children=navbar_items,
        brand="ITMO ML Service project",
        brand_href="#",
        color="primary",
        dark=True,
    )
    return navbar


def create_layout():
    navbar = create_navbar()
    app.layout = html.Div(
        [
            html.Div(navbar),
            dash.page_container,
            dcc.Store(id="session", storage_type="memory"),
        ]
    )


if __name__ == "__main__":
    create_layout()
    app.run(debug=True)
