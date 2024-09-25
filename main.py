from dash import Dash, html, dcc, Input, Output, State
import pandas as pd

# Import components
from components.Sidebar import Sidebar
from components.ProjectHeader import ProjectHeader

external_scripts = [
    {"src": "https://cdn.tailwindcss.com"},
    ]

external_stylesheets = [
    {"https://rsms.me/inter/inter.css"},
]

# Configuring Dash instance

app = Dash(__name__, 
           external_scripts=external_scripts,
           external_stylesheets=external_stylesheets
           )

# Dashboard Layout
app.layout = html.Div(
    className="w-screen h-screen flex",
    children= html.Div(
        className="flex flex-1",
        children = [
            Sidebar(),
            html.Div(
                className="flex flex-col w-full h-full p-9",
                children=[
                    html.Div(
                        children=ProjectHeader()
                    ),
                    html.Div(
                        className="grid",
                    )
                ]
            )
        ], 
    )
)



if __name__ == "__main__":
    app.run(debug=True, port="8051")