from dash import Dash, dcc, html, Input, Output, callback
import requests
import plotly.express as px

import pandas as pd

app = Dash(__name__)

slider_values = list(range(10, 15))
app.layout = html.Div(
    [
        dcc.Textarea(
            id="textarea-example",
            value="",
            style={"width": "100%", "height": 300},
        ),
        dcc.Slider(
            slider_values[0],
            slider_values[-1],
            step=1,
            value=slider_values[0],
            # marks=list(map(str, slider_values)),
            id="year-slider",
        ),
    ]
)


def read_item_by_id(id: int):
    output = requests.get(f"http://127.0.0.1:8000/items/{id}")
    return output.json()


@callback(Output("textarea-example", "value"), Input("year-slider", "value"))
def update_figure(selected_year):
    output = read_item_by_id(selected_year)
    print(output)
    return f"User has selected {output}]"


if __name__ == "__main__":
    app.run(debug=True)
