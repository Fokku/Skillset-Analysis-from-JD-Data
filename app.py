from dash import Dash, html, dcc, Input, Output, State
import pandas as pd

#Import data class
# from data.data import Data

# Import components
from components.Sidebar import Sidebar
from components.ProjectHeader import ProjectHeader

external_scripts = [
    {"src": "https://cdn.tailwindcss.com"},
    ]

external_stylesheets = [
    {"https://rsms.me/inter/inter.css"},
]

# Construct Data class
# data = Data().get_cleaned_table()

# Configuring Dash instance

app = Dash(__name__, 
           external_scripts=external_scripts,
           external_stylesheets=external_stylesheets
           )

server = app.server
# Fake static data for now
staticData = [
    {"title": "Total jobs", "value": "10,000"},
    {"title": "Total companies", "value": "1,000"},
    {"title": "Total job industries", "value": "100"},
    {"title": "Total job skills", "value": "500"},
]

def StaticDataCards(title="Title", value="Value"):
    return html.Div(
        className="p-6 transition-shadow border rounded-lg shadow-sm hover:shadow-lg",
        children=[
            html.Div(
                className="flex items-start justify-between",
                children=[
                    html.Div(
                        className="flex flex-col space-y-2",
                        children=[
                            html.Span(
                                className="text-lg text-slate-400",
                                children=title
                            ),
                            html.Span(
                                className="text-xl font-semibold text-slate-800",
                                children=value
                            )
                        ]
                    ),
                    html.Div(
                        className="p-10 bg-slate-200 rounded-md",
                        children=""
                    )
                ],
            ),
        ]
    )

def MainSection():
    return html.Div(
        className="grid grid-cols-1 gap-5 mt-6 sm:grid-cols-2 lg:grid-cols-4",
        children=[StaticDataCards(**data) for data in staticData]
    )

# Dashboard Layout
app.layout = html.Div(
    className="flex-1 max-h-full p-5 overflow-hidden overflow-y-scroll",
    children= html.Div(
        className="flex flex-1 h-screen",
        children = [
            Sidebar(),
            html.Main(
                className="flex flex-col w-full h-full p-9",
                children=[
                    html.Div(
                        children=ProjectHeader()
                    ),
                    MainSection(),

                ]
            )
        ], 
    )
)

# For dev
# app.run(debug=True, port="8051")

# For production
app.run_server(debug=False)