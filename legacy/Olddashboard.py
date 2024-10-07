import pandas as pd
from dash import Dash, dcc, html

# data = (
#     pd.read_csv("avocado.csv")
#     .query("type == 'conventional' and region == 'Albany'")
#     .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d"))
#     .sort_values(by="Date")
# )

data = pd.DataFrame(
    {
        "Date": ["2022-01-01", "2022-01-02", "2022-01-03", "2022-01-04"],
        "Total Volume": [1000, 1500, 1200, 1800],
        "AveragePrice": [1.5, 1.6, 1.4, 1.8],
        "SomeData": [10, 15, 12, 18],
        "AnotherData": [5, 8, 6, 9],
    }
)

app = Dash(__name__)


app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(children="Dashboard"),
                dcc.Dropdown(
                    ["Test1", "Test2", "Test3"],
                ),
            ],
            style={"display": "flex", "justify-content": "space-between"},
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        dcc.Graph(
                            figure={
                                "data": [
                                    {
                                        "x": data["Date"],
                                        "y": data["Total Volume"],
                                        "type": "lines",
                                    },
                                ],
                                "layout": {"title": "Avocados Sold"},
                            },
                        ),
                    ],
                    style={
                        "width": "25%",
                        "display": "inline-block",
                        "border": "1px solid black",
                        "padding": "10px",
                    },
                ),
                html.Div(
                    children=[
                        dcc.Graph(
                            figure={
                                "data": [
                                    {
                                        "x": data["Date"],
                                        "y": data["AveragePrice"],
                                        "type": "lines",
                                    },
                                ],
                                "layout": {"title": "Average Price of Avocados"},
                            },
                        ),
                    ],
                    style={
                        "width": "25%",
                        "display": "inline-block",
                        "border": "1px solid black",
                        "padding": "10px",
                    },
                ),
                html.Div(
                    children=[
                        dcc.Graph(
                            figure={
                                "data": [
                                    {
                                        "x": data["Date"],
                                        "y": data["SomeData"],
                                        "type": "lines",
                                    },
                                ],
                                "layout": {"title": "Some Data"},
                            },
                        ),
                    ],
                    style={
                        "width": "25%",
                        "display": "inline-block",
                        "border": "1px solid black",
                        "padding": "10px",
                    },
                ),
                html.Div(
                    children=[
                        dcc.Graph(
                            figure={
                                "data": [
                                    {
                                        "x": data["Date"],
                                        "y": data["AnotherData"],
                                        "type": "lines",
                                    },
                                ],
                                "layout": {"title": "Another Data"},
                            },
                        ),
                    ],
                    style={
                        "width": "25%",
                        "display": "inline-block",
                        "border": "1px solid black",
                        "padding": "10px",
                    },
                ),
            ],
            style={"display": "flex", "gap": "20"},
        ),
    ],
    style={"display": "flex", "flex-direction": "column", "gap": "6"},
)


app.run_server(debug=True)

# dcc.Graph(
#     figure={
#         "data": [
#             {
#                 "x": data["Date"],
#                 "y": data["Total Volume"],
#                 "type": "lines",
#             },
#         ],
#         "layout": {"title": "Avocados Sold"},
#     },
# ),
