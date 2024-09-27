from dash import Dash, html, dcc, Input, Output, State
import pandas as pd
import os

#Import data class
from data.data import Data

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
data = Data()
cleaned_data = data.get_cleaned_table()

# Configuring Dash instance

app = Dash(__name__, 
           external_scripts=external_scripts,
           external_stylesheets=external_stylesheets
           )
server = app.server

# Fake static data for now
staticData = [
    {"title": "Total jobs", "value": "10,000", "id": "total-jobs-pie"},
    {"title": "Total companies", "value": "1,000", "id": "total-companies-pie"},
    {"title": "Total job industries", "value": "100", "id": "total-industries-pie"},
    {"title": "Total job skills", "value": "500", "id": "total-skills-pie"},
]

def StaticDataCards(title="Title", value="Value", id="id"):
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
                        children=[
                            dcc.Graph(
                                id=id,
                                className="w-24 h-24"
                            )
                        ]
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

@app.callback(
    [
        Output('total-jobs-pie', 'figure'),
        Output('total-companies-pie', 'figure'),
        Output('total-industries-pie', 'figure'),
        Output('total-skills-pie', 'figure')
    ],
    [
        Input('region-filter', 'value'),
        Input('industry-filter', 'value')
    ]
)

def update_pie_charts(selected_region, selected_industry):
    filtered_df = cleaned_data[(cleaned_data['country'] == selected_region) & (cleaned_data['industry'] == selected_industry)]

    job_fig = {
        'data': [{'labels': ['Jobs'], 'values': [filtered_df['Jobs'].sum()], 'type': 'pie'}],
        'layout': {'title': 'Total Jobs'}
    }
    companies_fig = {
        'data': [{'labels': ['Companies'], 'values': [filtered_df['Companies'].sum()], 'type': 'pie'}],
        'layout': {'title': 'Total Companies'}
    }
    industries_fig = {
        'data': [{'labels': ['Industries'], 'values': [filtered_df['Industries'].sum()], 'type': 'pie'}],
        'layout': {'title': 'Total Industries'}
    }
    skills_fig = {
        'data': [{'labels': ['Skills'], 'values': [filtered_df['Skills'].sum()], 'type': 'pie'}],
        'layout': {'title': 'Total Skills'}
    }

    return job_fig, companies_fig, industries_fig, skills_fig

# For development only
# app.run(debug=True)

# For deployment
app.run(debug=True, host="0.0.0.0", port=os.getenv("PORT"))