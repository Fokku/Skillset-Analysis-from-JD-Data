from dash import Dash, html, dcc, Input, Output, State
import pandas as pd
from utils.time_utils import (
    convert_to_datetime,
    filter_recent_dates,
    group_by_time_and_skill,
)

# Import data class
from data.data import Data

data = Data()

# Import components
from components.Sidebar import Sidebar
from components.ProjectHeader import ProjectHeader
from components.StaticDataCards import StaticDataCards
from components.Seperator import Seperator
from components.MultiLineChart import MultiLineChart, InteractiveMultiLineChart
from components.Barchart import BarChart
from components.WordCloud import WordCloud

external_scripts = [
    {"src": "https://cdn.tailwindcss.com"},
]

external_stylesheets = [
    {"https://rsms.me/inter/inter.css"},
]

# Construct Data class
cleaned_data = data.get_cleaned_table()

# Configuring Dash instance

app = Dash(
    __name__,
    external_scripts=external_scripts,
    external_stylesheets=external_stylesheets,
)
server = app.server

# Skeleton data for static data cards
staticData = [
    {"title": "Total jobs", "value": cleaned_data.shape[0], "id": "total-jobs-pie"},
    {
        "title": "Total companies",
        "value": cleaned_data["company_name"].nunique(),
        "id": "total-companies-pie",
    },
    {
        "title": "Total job industries",
        "value": cleaned_data["industry_name"].nunique(),
        "id": "total-industries-pie",
    },
    {
        "title": "Total job skills",
        "value": cleaned_data["skill_name"].nunique(),
        "id": "total-skills-pie",
    },
]


def filter_data(df, selected_countries, selected_industries, selected_skills=None):
    filtered_df = df

    if selected_countries:
        if isinstance(selected_countries, str):
            selected_countries = [selected_countries]
        filtered_df = filtered_df[filtered_df["country"].isin(selected_countries)]

    if selected_industries:
        if isinstance(selected_industries, str):
            selected_industries = [selected_industries]
        filtered_df = filtered_df[
            filtered_df["industry_name"].isin(selected_industries)
        ]

    if selected_skills:
        if isinstance(selected_skills, str):
            selected_skills = [selected_skills]
        filtered_df = filtered_df[filtered_df["skill_name"].isin(selected_skills)]

    return filtered_df


def MainSection():
    return html.Div(
        id="main-section",
        className="",
        children=[
            html.Div(
                className="grid gap-5 mt-6 grid-cols-4",
                children=[StaticDataCards(**data) for data in staticData],
            ),
            html.Div(
                className="grid gap-2 mt-6 grid-cols-2",
                children=[
                    html.Div(
                        className="col-span-2 ",
                        children=[
                            html.H1(
                                className="text-lg text-center font-semibold text-slate-600",
                                children="Skillset Requirements Distribution",
                            ),
                            Seperator(className="my-2"),
                        ],
                    ),
                    BarChart(Title="Top 10 Highest In-Demand Skills"),
                    MultiLineChart(Title="Top 5 Skillset Demand Over Time"),
                    InteractiveMultiLineChart(
                        Title="Interactive Skillset Demand Over Time (Select Skills)"
                    ),
                ],
            ),
        ],
    )

# Add your graph components here
def MainSectionGeneralView():
    return html.Div(
        id="general-view",
        className="hidden",
        children=[
            html.Div(
                className="grid gap-2 mt-6 grid-cols-2",
                children=[
                    html.Div(
                        className="col-span-2 ",
                        children=[
                            html.H1(
                                className="text-lg text-center font-semibold text-slate-600",
                                children="General View",
                            ),
                            html.P(
                                className="text-sm text-center text-slate-600",
                                children="General view of the data, showing the distribution of job postings, companies, industries, and skills across the entire dataset.",
                            ),
                            Seperator(className="my-2"),
                        ],
                    ),
                    BarChart(
                        id="top-10-companies-job-postings",
                        Title="Top 10 Companies by Job Postings",
                        figure={
                            'data': [{
                                'type': 'bar',
                                'x': cleaned_data['company_name'].value_counts().nlargest(10).index,
                                'y': cleaned_data['company_name'].value_counts().nlargest(10).values
                            }],
                            'layout': {
                                'title': [
                                    html.H1(
                                        className="text-xl text-center font-semibold text-slate-800",
                                        children="Top 10 Companies by Job Postings",
                                    ),
                                ],
                                'xaxis': {'title': 'Company'},
                                'yaxis': {'title': 'Number of Job Postings'}
                            }
                        },
                    ),
                    html.Div(
                        className="p-4 transition-shadow border rounded-lg shadow-sm hover:shadow-lg",
                        children=[
                            dcc.Graph(
                                id="top-10-countries-jobs-postings",
                                figure={
                                    'data': [{
                                        'type': 'bar',
                                        'x': cleaned_data['country'].value_counts().nlargest(10).index,
                                        'y': cleaned_data['country'].value_counts().nlargest(10).values
                                    }],
                                    'layout': {
                                        'title': 'Top 10 Countries by Job Postings',
                                        'xaxis': {'title': 'Country'},
                                        'yaxis': {'title': 'Number of Job Postings'}
                                    }
                                },
                                className="w-full h-[300px]",
                                config={"displayModeBar": False},
                            ),
                        ]
                    ),
                    html.Div(
                        className="p-4 transition-shadow border rounded-lg shadow-sm hover:shadow-lg",
                        children=[
                            dcc.Graph(
                                id="salary-distribution-exp-level",
                                figure={
                                    'data': [
                                        {
                                            'type': 'box',
                                            'y': cleaned_data[cleaned_data['formatted_experience_level'] == level]['normalized_salary'],
                                            'name': level
                                        } for level in cleaned_data['formatted_experience_level'].unique()
                                    ],
                                    'layout': {
                                        'title': 'Salary Distribution by Experience Level',
                                        'yaxis': {'title': 'Normalized Salary'},
                                        'xaxis': {'title': 'Experience Level'}
                                    }
                                },
                                className="w-full h-[300px]",
                                config={"displayModeBar": False},
                            ),
                        ]
                    ),
                    html.Div(
                        className="p-4 transition-shadow border rounded-lg shadow-sm hover:shadow-lg",
                        children=[
                            dcc.Graph(
                                id="distribution of job postings by exp level",
                                figure={
                                    'data': [{
                                        'type': 'pie',
                                        'labels': cleaned_data['formatted_experience_level'].value_counts().index,
                                        'values': cleaned_data['formatted_experience_level'].value_counts().values
                                    }],
                                    'layout': {
                                        'title': 'Distribution of Job Postings by Experience Level'
                                    }
                                },
                                className="w-full h-[300px]",
                                config={"displayModeBar": False},
                            ),
                        ]
                    ),
                    html.Div(
                        className="p-4 transition-shadow border rounded-lg shadow-sm hover:shadow-lg",
                        children=[
                            dcc.Graph(
                                id="salary distribution by country",
                                figure={
                                    'data': [
                                        {
                                            'type': 'box',
                                            'y': cleaned_data[cleaned_data['country'] == country]['normalized_salary'],
                                            'name': country
                                        } for country in cleaned_data['country'].value_counts().nlargest(10).index
                                    ],
                                    'layout': {
                                        'title': 'Salary Distribution by Top 10 Countries',
                                        'yaxis': {'title': 'Normalized Salary'},
                                        'xaxis': {'title': 'Country'}
                                    }
                                },
                                className="w-full h-[300px]",
                                config={"displayModeBar": False},
                            ),
                        ]
                    ),
                    html.Div(
                        className="p-4 transition-shadow border rounded-lg shadow-sm hover:shadow-lg",
                        children=[
                            dcc.Graph(
                                id="Top 10 Highest Paying Industries based on Median Salary",
                                figure={
                                    'data': [{
                                        'type': 'bar',
                                        'x': cleaned_data.groupby('industry_name')['normalized_salary'].median().nlargest(10).index,
                                        'y': cleaned_data.groupby('industry_name')['normalized_salary'].median().nlargest(10).values
                                    }],
                                    'layout': {
                                        'title': 'Top 10 Highest Paying Industries (Median Salary)',
                                        'xaxis': {'title': 'Industry'},
                                        'yaxis': {'title': 'Median Normalized Salary'}
                                    }
                                },
                                className="w-full h-[300px]",
                                config={"displayModeBar": False},
                            ),
                        ]
                    ),
                    html.Div(
                        className="p-4 transition-shadow border rounded-lg shadow-sm hover:shadow-lg",
                        children=[
                            dcc.Graph(
                                id="Top 10 Highest Paying Companies based on Median Salary",
                                figure={
                                    'data': [{
                                        'type': 'bar',
                                        'x': cleaned_data.groupby('company_name')['normalized_salary'].median().nlargest(10).index,
                                        'y': cleaned_data.groupby('company_name')['normalized_salary'].median().nlargest(10).values
                                    }],
                                    'layout': {
                                        'title': 'Top 10 Highest Paying Companies (Median Salary)',
                                        'xaxis': {'title': 'Company'},
                                        'yaxis': {'title': 'Median Normalized Salary'}
                                    }
                                },
                                className="w-full h-[300px]",
                                config={"displayModeBar": False},
                            ),
                        ]
                    ),
                    html.Div(
                        className="p-4 transition-shadow border rounded-lg shadow-sm hover:shadow-lg",
                        children=[
                            dcc.Graph(
                                id="Top 10 most in-demand skills across all industries",
                                figure={
                                    'data': [{
                                        'type': 'bar',
                                        'x': cleaned_data['skill_name'].value_counts().nlargest(10).index,
                                        'y': cleaned_data['skill_name'].value_counts().nlargest(10).values
                                    }],
                                    'layout': {
                                        'title': 'Top 10 Most In-Demand Skills',
                                        'xaxis': {'title': 'Skill'},
                                        'yaxis': {'title': 'Number of Job Postings'}
                                    }
                                },
                                className="w-full h-[300px]",
                                config={"displayModeBar": False},
                            ),
                        ]
                    ),
                    WordCloud(
                        data=cleaned_data['skill_name'].value_counts().nlargest(100).to_dict(),
                        Title="Most In-Demand Skills",
                        id="most-skills-wordcloud",
                    )
                ],
            )
        ],
    )


# Dashboard Layout
app.layout = html.Div(
    className="flex-1 max-h-screen p-5",
    children=html.Div(
        className="flex flex-1 h-screen overflow-hidden",
        children=[
            Sidebar(),
            html.Main(
                className="flex flex-col w-full h-full p-9 overflow-hidden overflow-y-scroll",
                children=[
                    html.Div(children=ProjectHeader()),
                    MainSection(),
                    MainSectionGeneralView(),
                ],
            ),
        ],
    ),
)


# Toggle between main section and general view
@app.callback(
    [
        Output("main-section", "className"),
        Output("general-view", "className"),
        Output("country-filter", "disabled"),
        Output("industry-filter", "disabled"),
    ],
    [Input("general-view-toggle", "value")],
)
def update_main_section(general_view):
    if general_view:
        return "hidden", "block", True, True
    else:
        return "block", "hidden", False, False


# Update pie charts
@app.callback(
    [
        Output("total-jobs-pie", "figure"),
        Output("total-companies-pie", "figure"),
        Output("total-industries-pie", "figure"),
        Output("total-skills-pie", "figure"),
    ],
    [Input("country-filter", "value"), Input("industry-filter", "value")],
)
def update_pie_charts(selected_countries, selected_industries):

    filtered_df = filter_data(cleaned_data, selected_countries, selected_industries)

    total_jobs = len(filtered_df)
    total_companies = filtered_df["company_name"].nunique()
    total_industries = filtered_df["industry_name"].nunique()
    total_skills = filtered_df["skill_name"].nunique()

    # Create pie charts
    job_fig = {
        "data": [
            {
                "labels": ["Jobs", "Other Jobs"],
                "values": [total_jobs, len(cleaned_data) - total_jobs],
                "type": "pie",
            }
        ],
        "layout": {"showlegend": False, "margin": dict(l=0, r=0, t=0, b=0)},
    }
    companies_fig = {
        "data": [
            {
                "labels": ["Companies", "Other Companies"],
                "values": [
                    total_companies,
                    cleaned_data["company_name"].nunique() - total_companies,
                ],
                "type": "pie",
            }
        ],
        "layout": {"showlegend": False, "margin": dict(l=0, r=0, t=0, b=0)},
    }
    industries_fig = {
        "data": [
            {
                "labels": ["Industries", "Other Industries"],
                "values": [
                    total_industries,
                    cleaned_data["industry_name"].nunique() - total_industries,
                ],
                "type": "pie",
            }
        ],
        "layout": {"showlegend": False, "margin": dict(l=0, r=0, t=0, b=0)},
    }
    skills_fig = {
        "data": [
            {
                "labels": ["Skills", "Other Skills"],
                "values": [
                    total_skills,
                    cleaned_data["skill_name"].nunique() - total_skills,
                ],
                "type": "pie",
            }
        ],
        "layout": {"showlegend": False, "margin": dict(l=0, r=0, t=0, b=0)},
    }

    return job_fig, companies_fig, industries_fig, skills_fig


# Update time-series charts
@app.callback(
    [
        Output("interactive-skills-over-time-chart", "figure"),
        Output("skills-over-time-chart", "figure"),
    ],
    [
        Input("country-filter", "value"),
        Input("industry-filter", "value"),
        Input("skill-filter", "value"),
    ],
)
def update_time_series_charts(selected_countries, selected_industries, selected_skills):
    # Filter data based on country and industry
    filtered_df = filter_data(
        cleaned_data,
        selected_countries,
        selected_industries,
    )

    # Convert and filter dates
    filtered_df = convert_to_datetime(filtered_df, "original_listed_time")
    filtered_df = filter_recent_dates(filtered_df, "listed_date", days=210)

    # Create multi-line chart for top 5 skillset requirements over time
    skills_over_time, top_5_skills = group_by_time_and_skill(
        filtered_df, "listed_date", "skill_name"
    )

    skills_over_time_fig = {
        "data": [
            {
                "x": skills_over_time.index,
                "y": skills_over_time[skill],
                "type": "scatter",
                "mode": "lines",
                "name": skill,
                "line": {"shape": "linear", "smoothing": 0.4},
            }
            for skill in top_5_skills
        ],
        "layout": {
            "title": "Top 5 Skills Over Time",
            "xaxis": {
                "tickformat": "%Y-%m-%d",
                "tickangle": 45,
            },
            "yaxis": {"title": "Skill Mentions"},
            "legend": {"orientation": "h", "y": -0.5},
            "hovermode": "closest",
            "margin": {"b": 100, "t": 30, "l": 60, "r": 30},
        },
    }

    # Create interactive skills chart
    if selected_skills:
        # Filter data again, this time including the selected skills
        interactive_filtered_df = filter_data(
            filtered_df,
            selected_countries,
            selected_industries,
            selected_skills=selected_skills,
        )
        interactive_skills_over_time, _ = group_by_time_and_skill(
            interactive_filtered_df, "listed_date", "skill_name"
        )
        interactive_skills = selected_skills
    else:
        interactive_skills_over_time = skills_over_time
        interactive_skills = top_5_skills

    interactive_skills_fig = {
        "data": [
            {
                "x": interactive_skills_over_time.index,
                "y": interactive_skills_over_time[skill],
                "type": "scatter",
                "mode": "lines",
                "name": skill,
                "line": {"shape": "linear", "smoothing": 0.4},
            }
            for skill in interactive_skills
        ],
        "layout": {
            "title": "Interactive Skills Over Time",
            "xaxis": {
                "tickformat": "%Y-%m-%d",
                "tickangle": 45,
            },
            "yaxis": {"title": "Skill Mentions"},
            "legend": {"orientation": "h", "y": -0.5},
            "hovermode": "closest",
            "margin": {"b": 100, "t": 30, "l": 60, "r": 30},
        },
    }

    return interactive_skills_fig, skills_over_time_fig


# Update bar chart, multi-line chart, and other data
@app.callback(
    [
        Output("top-skills-barchart", "figure"),
        Output("total-jobs-pie-value", "children"),
        Output("total-companies-pie-value", "children"),
        Output("total-industries-pie-value", "children"),
        Output("total-skills-pie-value", "children"),
        Output("skill-filter", "options"),
    ],
    [Input("country-filter", "value"), Input("industry-filter", "value")],
)
def update_charts(selected_countries, selected_industries):

    filtered_df = filter_data(cleaned_data, selected_countries, selected_industries)

    total_jobs = len(filtered_df)
    total_companies = filtered_df["company_name"].nunique()
    total_industries = filtered_df["industry_name"].nunique()
    total_skills = filtered_df["skill_name"].nunique()
    skills_list = filtered_df["skill_name"].unique().tolist()

    # Create bar chart for top 5 skills
    top_skills = filtered_df["skill_name"].value_counts().nlargest(10)
    skills_bar_fig = {
        "data": [{"x": top_skills.index, "y": top_skills.values, "type": "bar"}],
        "layout": {
            #'xaxis': {'title': 'Skills'},
            "yaxis": {"title": "Count"},
        },
    }

    return (
        skills_bar_fig,
        f"{total_jobs:,}",
        f"{total_companies:,}",
        f"{total_industries:,}",
        f"{total_skills:,}",
        [{"label": skill, "value": skill} for skill in skills_list],
    )

# TODO: Fix sidebar toggle

# @app.callback(
#     [Output("sidebar", "className")],
#     [Input("toggle-sidebar-button", "n_clicks")],
# )
# def toggle_sidebar(n_clicks):
#     if n_clicks:
#         return ["hidden"]
#     else:
#         return ["flex"]

# For development only
# app.run(debug=True)

# For deployment
app.run(debug=True, host="0.0.0.0", port=8000)