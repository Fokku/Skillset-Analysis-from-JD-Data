from dash import Dash, html, dcc, Input, Output, State
import os
import pandas as pd

# Import data class
from data.data import Data
data = Data()

# Import utils
from utils.time_utils import (
    convert_to_datetime,
    filter_recent_dates,
    group_by_time_and_skill,
)
from utils.filter_data import filter_data

# Import components
from components.Sidebar import Sidebar
from components.ProjectHeader import ProjectHeader
from components.StaticDataCards import StaticDataCards
from components.Seperator import Seperator
from components.MultiLineChart import MultiLineChart, InteractiveMultiLineChart
from components.Barchart import BarChart
from components.Piechart import Piechart
from components.WordCloud import WordCloud
from components.Boxchart import Boxchart

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

# Layout for static data cards
staticDataLayout = [
    {"title": "Jobs", "value": cleaned_data.shape[0], "id": "total-jobs-pie"},
    {
        "title": "Companies",
        "value": cleaned_data["company_name"].nunique(),
        "id": "total-companies-pie",
    },
    {
        "title": "Job industries",
        "value": cleaned_data["industry_name"].nunique(),
        "id": "total-industries-pie",
    },
    {
        "title": "Skill Keywords",
        "value": cleaned_data["skill_name"].nunique(),
        "id": "total-skills-pie",
    },
]


def MainSection():
    return html.Div(
        id="main-section",
        className="",
        children=[
            html.Div(
                className="grid gap-5 mt-6 grid-cols-4",
                children=[StaticDataCards(**data) for data in staticDataLayout],
            ),
            html.Div(
                className="grid gap-2 mt-6 grid-cols-2",
                children=[
                    BarChart(Title="Skill Keyword Frequency", id="top-skills-barchart", description="Aggregation of the top 10 highest in-demand skills"),
                    BarChart(Title="Companies by Job Posting Count", id="top-10-hiring-companies", description="Top 10 hiring companies by number of job postings"),
                    # MultiLineChart(Title="Top 5 Skillset Demand Over Time"),
                    InteractiveMultiLineChart(
                        Title="Skillset Demand Over Time (Select Skills)"
                    ),
                    BarChart(Title="Distribution of Employment Types", id="employment-types-bar"),
                    Piechart(Title="Remote vs Onsite Positions", id="remote-vs-onsite-pie"),
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
                        figure={
                            'data': [{
                                'type': 'bar',
                                'x': cleaned_data['company_name'].value_counts().nlargest(10).index,
                                'y': cleaned_data['company_name'].value_counts().nlargest(10).values
                            }],
                            'layout': {
                                'title': 'Top 10 Companies by Job Postings',
                                'xaxis': {'title': 'Company'},
                                'yaxis': {'title': 'Number of Job Postings'}
                            }
                        },
                    ),
                    Boxchart(
                        id="salary-distribution-exp-level",
                        description="Distribution of salaries by experience level",
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
                    ),
                    Piechart(
                        id="distribution-of-job-postings-by-exp-level-pie",
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
                    ),
                    Piechart(
                        id="distribution-of-job-postings-by-industry-pie",
                        figure={
                            'data': [{
                                'type': 'pie',
                                'labels': cleaned_data['industry_name'].value_counts().nlargest(10).index,
                                'values': cleaned_data['industry_name'].value_counts().nlargest(10).values
                            }],
                            'layout': {
                                'title': 'Top 10 Distribution of Job Postings by Industry'
                            }
                        },
                    ),
                    
                    Piechart(
                        id="distribution-of-job-postings-by-work-type-pie",
                        figure={
                            'data': [{
                                'type': 'pie',
                                'labels': cleaned_data['formatted_work_type'].value_counts().index,
                                'values': cleaned_data['formatted_work_type'].value_counts().values
                            }],
                            'layout': {
                                'title': 'Distribution of Job Postings by Work Type'
                            }
                        },
                    ),

                    Boxchart(
                        id="salary-distribution-country",
                        description="Distribution of salaries by country",
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
                    ),
                    BarChart(
                        id="top-10-highest-paying-industries-bar",
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
                    ),
                    BarChart(
                        id="top-10-highest-paying-companies-bar",
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
                    ),

                    BarChart(
                        id="top-10-most-in-demand-skills-bar",
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
                    ),
                    # WordCloud(
                    #     data=cleaned_data['skill_name'].value_counts().nlargest(100).to_dict(),
                    #     Title="Most In-Demand Skills",
                    #     id="most-skills-wordcloud",
                    # ),
                    Boxchart(
                        id="salary-distribution-job-roles",
                        description="Distribution of salaries by top 10 job roles",
                        figure={
                            'data': [
                                {
                                    'type': 'box',
                                    'y': cleaned_data[cleaned_data['title'] == role]['normalized_salary'],
                                    'name': role,
                                    'boxpoints': 'outliers'
                                } for role in cleaned_data['title'].value_counts().nlargest(10).index
                            ],
                            'layout': {
                                'title': 'Salary Distribution by Top 10 Job Roles',
                                'yaxis': {'title': 'Normalized Salary'},
                                'xaxis': {'title': 'Job Role'},
                                'showlegend': False
                            }
                        },
                    ),
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
        Output("employment-types-bar", "figure"),
        Output("remote-vs-onsite-pie", "figure"),
    ],
    [Input("country-filter", "value"), Input("industry-filter", "value")],
)
def update_pie_charts(selected_countries, selected_industries):

    filtered_df = filter_data(cleaned_data, selected_countries, selected_industries)

    # Get total counts for total-jobs-pie, total-companies-pie, total-industries-pie, and total-skills-pie
    total_jobs = len(filtered_df)
    total_companies = filtered_df["company_name"].nunique()
    total_industries = filtered_df["industry_name"].nunique()
    total_skills = filtered_df["skill_name"].nunique()

    # Helper function to generate figure objects for pie charts
    def pie_fig_generator(data, labels, colors, hole=None, **kwargs):
        return {
            "data": [
                {
                    "labels": labels,
                    "values": data,
                    "type": "pie",
                    "hole": hole,
                    "marker": {"colors": colors},
                }
            ],
            "layout": {"showlegend": False, "margin": dict(l=0, r=0, t=0, b=0), **kwargs}
        }

    # Consistent colors for each pie chart
    colours = ['#4C8FBA', '#DE663E']

    # Create pie charts
    job_fig = pie_fig_generator([total_jobs, len(cleaned_data) - total_jobs], ["Jobs", "Other Jobs"], colours)
    companies_fig = pie_fig_generator([total_companies, cleaned_data["company_name"].nunique() - total_companies], ["Companies", "Other Companies"], colours)
    industries_fig = pie_fig_generator([total_industries, cleaned_data["industry_name"].nunique() - total_industries], ["Industries", "Other Industries"], colours)
    skills_fig = pie_fig_generator([total_skills, cleaned_data["skill_name"].nunique() - total_skills], ["Skills", "Other Skills"], colours)

    employment_types = filtered_df['formatted_work_type'].value_counts()
    employment_types_fig = {
        'data': [{
            'type': 'bar',
            'x': employment_types.index,
            'y': employment_types.values,
            'marker': {'color': '#DE663E'},
        }],
        'layout': {
            'xaxis': {'title': 'Employment Type'},
            'yaxis': {'title': 'Number of Jobs'},
            'margin': {'l': 50, 'r': 50, 't': 50, 'b': 100},
        }
    }
    
    remote_onsite_counts = filtered_df['remote_allowed'].map({'Unknown': 'On-site', 1.0: 'Remote', "1.0": "Remote", True: "Remote"}).value_counts()
    remote_onsite_fig = pie_fig_generator(
        remote_onsite_counts.values.tolist(),
        remote_onsite_counts.index.tolist(),
        colours,
        hole=0.3,
    )

    return job_fig, companies_fig, industries_fig, skills_fig, employment_types_fig, remote_onsite_fig


# Update time-series charts
@app.callback(
    [
        Output("interactive-skills-over-time-chart", "figure"),
        # Output("skills-over-time-chart", "figure"),
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

    # skills_over_time_fig = {
    #     "data": [
    #         {
    #             "x": skills_over_time.index,
    #             "y": skills_over_time[skill],
    #             "type": "scatter",
    #             "mode": "lines",
    #             "name": skill,
    #             "line": {"shape": "linear", "smoothing": 0.4},
    #         }
    #         for skill in top_5_skills
    #     ],
    #     "layout": {
    #         "title": "Top 5 Skills Over Time",
    #         "xaxis": {
    #             "tickformat": "%Y-%m-%d",
    #             "tickangle": 45,
    #         },
    #         "yaxis": {"title": "Skill Mentions"},
    #         "legend": {"orientation": "h", "y": -0.5},
    #         "hovermode": "closest",
    #         "margin": {"b": 100, "t": 30, "l": 60, "r": 30},
    #     },
    # }

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
                "animation_frame": "listed_date"
            }
            for skill in interactive_skills
        ],
        "layout": {
            "xaxis": {
                "tickformat": "%Y-%m-%d",
                "tickangle": 45,
            },
            "yaxis": {"title": "Skill Mentions"},
            "legend": {"orientation": "h", "y": -0.5},
            "hovermode": "closest",
            "margin": {"b": 100, "t": 30, "l": 60, "r": 30}
        },
    }

    return interactive_skills_fig, #skills_over_time_fig


# Update bar chart, multi-line chart, and other data
@app.callback(
    [
        Output("top-skills-barchart", "figure"),
        Output("top-10-hiring-companies", "figure"),
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
            'xaxis': {'title': 'Skills'},
            "yaxis": {"title": "Count"},
            'margin': {'l': 50, 'r': 50, 't': 50, 'b': 100},
        },
    }

    top_10_hiring_companies = filtered_df.groupby('company_name').size().nlargest(10).reset_index(name='count')
    top_10_hiring_companies_fig = {
        "data": [{"x": top_10_hiring_companies['company_name'], "y": top_10_hiring_companies['count'], "type": "bar"}],
        "layout": {
            "xaxis": {"title": "Company Name"},
            "yaxis": {"title": "Number of Jobs Posted"},
            'margin': {'l': 50, 'r': 50, 't': 50, 'b': 100},
        }
    }

    return (
        skills_bar_fig,
        top_10_hiring_companies_fig,
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

# Run the app
if os.environ.get("ENV") == "dev":
    app.run(debug=True, port=8000)
else:
    app.run(debug=False, host="0.0.0.0", port=8000)