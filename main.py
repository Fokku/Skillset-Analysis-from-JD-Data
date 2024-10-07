from dash import Dash, html, dcc, Input, Output, State
import pandas as pd
from utils.time_utils import convert_to_datetime, filter_recent_dates, group_by_time_and_skill
import os
from datetime import datetime, timedelta

# Import data class
from data.data import Data

# Import components
from components.Sidebar import Sidebar
from components.ProjectHeader import ProjectHeader
from components.StaticDataCards import StaticDataCards
from components.Seperator import Seperator

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

# Skeleton data for static data cards
staticData = [
    {
        "title": "Total jobs", 
        "value": cleaned_data.shape[0], 
        "id": "total-jobs-pie"
    },
    {
        "title": "Total companies", 
        "value": cleaned_data['company_name'].nunique(), 
        "id": "total-companies-pie"
    },
    {
        "title": "Total job industries", 
        "value": cleaned_data['industry_name'].nunique(), 
        "id": "total-industries-pie"
    },
    {
        "title": "Total job skills", 
        "value": cleaned_data['skill_name'].nunique(), 
        "id": "total-skills-pie"
    },
]

def filter_data(df, selected_countries, selected_industries):
    filtered_df = df

    if selected_countries:
        if isinstance(selected_countries, str):
            selected_countries = [selected_countries]
        filtered_df = filtered_df[filtered_df['country'].isin(selected_countries)]
    
    if selected_industries:
        if isinstance(selected_industries, str):
            selected_industries = [selected_industries]
        filtered_df = filtered_df[filtered_df['industry_name'].isin(selected_industries)]
    
    return filtered_df
    

def BarChart(Title="Top 10 Skills"):
    return html.Div(
        className="p-4 transition-shadow border rounded-lg shadow-sm hover:shadow-lg",
        children=[
            html.H1(
                className="text-xl text-center font-semibold text-slate-800",
                children=Title
            ),
            dcc.Graph(
                id="top-skills-barchart",
                className="w-full h-[300px]",
                config={
                    'displayModeBar': False
                }
            )
        ]
    )

def MultiLineChart(Title="Skillset Requirements Over Time"):
    return html.Div(
        className="p-4 transition-shadow border rounded-lg shadow-sm hover:shadow-lg",
        children=[
            html.H1(
                className="text-xl text-center font-semibold text-slate-800",
                children=Title
            ),
            dcc.Graph(
                id="skills-over-time-chart",
                className="w-full h-[300px]",
                config={
                    'displayModeBar': False
                }
            )
        ]
    )

def InteractiveMultiLineChart(Title="Skillset Requirements Over Time"):
    return html.Div(
        className="col-span-2 p-4 transition-shadow border rounded-lg shadow-sm hover:shadow-lg",
        children=[
            html.H1(
                className="text-xl text-center font-semibold text-slate-800",
                children=Title
            ),
            html.Div(
                className="flex flex-row justify-end",
                children=[
                    dcc.Dropdown(
                        id="skill-filter",
                        className="w-1/2",
                        options=[],
                        multi=True,
                    )
                ]
            ),
            dcc.Graph(
                id="interactive-skills-over-time-chart",
                className="w-full h-[300px]",
                config={
                    'displayModeBar': False
                }
            )
        ]
    )

def MainSection():
    return html.Div(
        id="main-section",
        className="",
        children=[
            html.Div(
                className="grid gap-5 mt-6 grid-cols-4",
                children=[StaticDataCards(**data) for data in staticData]
            ),
            html.Div(
                className="grid gap-2 mt-6 grid-cols-2",
                children=[
                    html.Div(
                        className="col-span-2 ",
                        children=[
                            html.H1(
                                className="text-lg text-center font-semibold text-slate-600",
                                children="Skillset Requirements Distribution"
                            ),
                            Seperator(className="my-2")
                        ]
                    ),
                    BarChart(Title="Top 10 Skills"),
                    MultiLineChart(Title="Skillset Requirements Over Time"),
                    InteractiveMultiLineChart(Title="Test"),
                ]
            )
        ]
    )

def MainSectionGeneralView():
    return html.Div(
        id="general-view",
        className="",
        children=[
            'general view'
        ]
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
        Output('main-section', 'className'),
        Output('general-view', 'className'),
        Output('country-filter', 'disabled'),
        Output('industry-filter', 'disabled')
    ],
    [
        Input('general-view-toggle', 'value')
    ]
)
def update_main_section(general_view):
    if general_view:
        return "hidden", "block", True, True
    else:
        return "block", "hidden", False, False

@app.callback(
    [
        Output('total-jobs-pie', 'figure'),
        Output('total-companies-pie', 'figure'),
        Output('total-industries-pie', 'figure'),
        Output('total-skills-pie', 'figure'),
    ],
    [
        Input('country-filter', 'value'),
        Input('industry-filter', 'value')
    ]
)
def update_pie_charts(selected_countries, selected_industries):

    filtered_df = filter_data(cleaned_data, selected_countries, selected_industries)

    total_jobs = len(filtered_df)
    total_companies = filtered_df['company_name'].nunique()
    total_industries = filtered_df['industry_name'].nunique()
    total_skills = filtered_df['skill_name'].nunique()

    # Create pie charts
    job_fig = {
        'data': [{'labels': ['Jobs', 'Other Jobs'], 'values': [total_jobs, len(cleaned_data) - total_jobs], 'type': 'pie'}],
        'layout': {'showlegend': False, 'margin': dict(l=0, r=0, t=0, b=0)}
    }
    companies_fig = {
        'data': [{'labels': ['Companies', 'Other Companies'], 'values': [total_companies, cleaned_data['company_name'].nunique() - total_companies], 'type': 'pie'}],
        'layout': {'showlegend': False, 'margin': dict(l=0, r=0, t=0, b=0)}
    }
    industries_fig = {
        'data': [{'labels': ['Industries', 'Other Industries'], 'values': [total_industries, cleaned_data['industry_name'].nunique() - total_industries], 'type': 'pie'}],
        'layout': {'showlegend': False, 'margin': dict(l=0, r=0, t=0, b=0)}
    }
    skills_fig = {
        'data': [{'labels': ['Skills', 'Other Skills'], 'values': [total_skills, cleaned_data['skill_name'].nunique() - total_skills], 'type': 'pie'}],
        'layout': {'showlegend': False, 'margin': dict(l=0, r=0, t=0, b=0)}
    }

    return job_fig, companies_fig, industries_fig, skills_fig

@app.callback(
    [
        Output('top-skills-barchart', 'figure'),
        Output('skills-over-time-chart', 'figure'),
        Output('total-jobs-pie-value', 'children'),
        Output('total-companies-pie-value', 'children'),
        Output('total-industries-pie-value', 'children'),
        Output('total-skills-pie-value', 'children'),
        Output('skills-filter', 'options')
    ],
    [
        Input('country-filter', 'value'),
        Input('industry-filter', 'value')
    ]
)
def update_charts(selected_countries, selected_industries):

    filtered_df = filter_data(cleaned_data, selected_countries, selected_industries)

    # Convert and filter dates
    filtered_df = convert_to_datetime(filtered_df, 'original_listed_time')
    filtered_df = filter_recent_dates(filtered_df, 'listed_date', days=210)

    total_jobs = len(filtered_df)
    total_companies = filtered_df['company_name'].nunique()
    total_industries = filtered_df['industry_name'].nunique()
    total_skills = filtered_df['skill_name'].nunique()

    skills_list = filtered_df['skill_name'].unique().tolist()

    # Create bar chart for top 5 skills
    top_skills = filtered_df['skill_name'].value_counts().nlargest(10)
    skills_bar_fig = {
        'data': [{
            'x': top_skills.index,
            'y': top_skills.values,
            'type': 'bar'
        }],
        'layout': {
            #'xaxis': {'title': 'Skills'},
            'yaxis': {'title': 'Count'},
        }
    }
    
    # Create multi-line chart for skillset requirements over time
    skills_over_time, top_5_skills = group_by_time_and_skill(filtered_df, 'listed_date', 'skill_name')

    skills_over_time_fig = {
        'data': [
            {
                'x': skills_over_time.index,
                'y': skills_over_time[skill],
                'type': 'scatter',
                'mode': 'lines',
                'name': skill,
                'line': {
                    'shape': 'linear',
                    'smoothing': 0.4
                }
            } for skill in top_5_skills
        ],
        'layout': {
            'xaxis': {
                'tickformat': '%Y-%m-%d',
                'tickangle': 45,
            },
            'yaxis': {'title': 'Skillset Mentions'},
            'legend': {'orientation': 'h', 'y': -0.2},
            'hovermode': 'closest',
            'margin': {'b': 40, 't': 0, 'l': 40, 'r': 0, 'pad': 0},
            # 'width': 1000
        }
    }
    
    return skills_bar_fig, skills_over_time_fig, f"{total_jobs:,}", f"{total_companies:,}", f"{total_industries:,}", f"{total_skills:,}, {skills_list}"

# For development only
# app.run(debug=True)

# For deployment
app.run(debug=True, host="0.0.0.0", port=8000)