from dash import Dash, html, dcc, Input, Output, State
import pandas as pd
import pandas as pd
import html as hyper
from components.API import get_skill_description, get_youtube_videos
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
    suppress_callback_exceptions=True
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


def filter_data(df, selected_countries, selected_industries, **kwargs):
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

    if kwargs.get("selected_skills"):
        if isinstance(kwargs.get("selected_skills"), str):
            selected_skills = [kwargs.get("selected_skills")]
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
                            Seperator(className="my-2"),
                        ],
                    ),
                    BarChart(
                        id="top-10-companies-job-postings",
                        Title="Top 10 Companies by Job Postings",
                    ),
                    dcc.Graph(
                        id="top-10-countries-jobs-postings",
                        className="w-full h-[300px]",
                        config={"displayModeBar": False},
                    ),
                    dcc.Graph(
                        id="salary-distribution-exp-level",
                        className="w-full h-[300px]",
                        config={"displayModeBar": False},
                    ),
                    dcc.Graph(
                        id="distribution of job postings by exp level",
                        className="w-full h-[300px]",
                        config={"displayModeBar": False},
                    ),
                    dcc.Graph(
                        id="salary distribution by country",
                        className="w-full h-[300px]",
                        config={"displayModeBar": False},
                    ),
                    dcc.Graph(
                        id="Top 10 Highest Paying Industries based on Median Salary",
                        className="w-full h-[300px]",
                        config={"displayModeBar": False},
                    ),
                    dcc.Graph(
                        id="Top 10 Highest Paying Companies based on Median Salary",
                        className="w-full h-[300px]",
                        config={"displayModeBar": False},
                    ),
                    dcc.Graph(
                        id="Top 10 most in-demand skills across all industries",
                        className="w-full h-[300px]",
                        config={"displayModeBar": False},
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


# Update time-series chart
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
    filtered_df = filter_data(
        cleaned_data,
        selected_countries,
        selected_industries,
        selected_skills=selected_skills,
    )

    # Convert and filter dates
    filtered_df = convert_to_datetime(filtered_df, "original_listed_time")
    filtered_df = filter_recent_dates(filtered_df, "listed_date", days=210)

    # Create multi-line chart for skillset requirements over time
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
                "title": "Date",
                "tickformat": "%Y-%m-%d",
                "tickangle": 45,
            },
            "yaxis": {"title": "Skill Mentions"},
            "legend": {"orientation": "h", "y": -0.2},
            "hovermode": "closest",
            "margin": {"b": 100, "t": 30, "l": 60, "r": 30},
        },
    }

    # Create interactive skills chart
    if selected_skills:
        interactive_skills = selected_skills
    else:
        interactive_skills = top_5_skills

    interactive_skills_fig = {
        "data": [
            {
                "x": skills_over_time.index,
                "y": skills_over_time[skill],
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
                "title": "Date",
                "tickformat": "%Y-%m-%d",
                "tickangle": 45,
            },
            "yaxis": {"title": "Skill Mentions"},
            "legend": {"orientation": "h", "y": -0.2},
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

# Callback to display the initial page or the chart
@app.callback(
    Output('main-content', 'children'),
    Input('page-url', 'pathname')  # URL tracker input
)
def display_page(pathname):

    # Display the home page (main sections) when on '/'
    if pathname == '/':
        return html.Div(
            children=[
                MainSection(),  # Show the main sections when on home page
                MainSectionGeneralView(),
            ]
        )

    # Display skill details when the URL starts with '/skills/'
    elif pathname.startswith('/skills/'):
        # Extract skill name from the URL and decode it to handle special characters
        skill_name_encoded = pathname.split('/skills/')[-1]
        skill_name = unquote(skill_name_encoded).replace('-', ' ')  # Decode URL and replace hyphens with spaces

        # Check if the skill exists in the DataFrame
        df_filtered = cleaned_data[cleaned_data["skill_name"].str.contains(skill_name, case=False, na=False)]

        # If the skill does not exist, display an error message
        if df_filtered.empty:
            return html.Div([
                html.H2("Skill not found"),
                html.P(f"The skill '{skill_name}' does not exist in our data."),
                html.P("Please check your input or go back to the home page.")
            ])

        description = get_skill_description(skill_name)

        # Filter the DataFrame for rows that contain the selected skill
        df_filtered = cleaned_data[cleaned_data["skill_name"].str.contains(skill_name, case=False, na=False)].copy()

        # Convert 'listed_time' from Unix timestamp to datetime format
        df_filtered['listed_time'] = pd.to_datetime(df_filtered['listed_time'], unit='ms')

        # Extract day from 'listed_time'
        df_filtered['day'] = df_filtered['listed_time'].dt.to_period('D')

        # Group by 'day' to get job counts for each day
        job_counts_by_day = df_filtered.groupby('day').size().reset_index(name='job_count')

        print(job_counts_by_day)

        # Create the Plotly line chart
        individualSkill_over_time_fig = {
            "data": [
                {
                    "x": job_counts_by_day['day'].astype(str),  # Convert PeriodIndex to string for JSON serialization
                    "y": job_counts_by_day['job_count'],
                    "type": "scatter",
                    "mode": "lines",
                    "name": skill_name,
                    "line": {"shape": "linear", "smoothing": 0.4},
                }
            ],
            "layout": {
                "title": f"Job Postings for {skill_name} Over Time (Daily)",
                "xaxis": {
                    "title": "Date",
                    "tickformat": "%Y-%m-%d",  # Tick format adjusted for day level
                    "tickangle": 45,
                },
                "yaxis": {"title": "Job Postings"},
                "legend": {"orientation": "h", "y": -0.2},
                "hovermode": "closest",
                "margin": {"b": 100, "t": 30, "l": 60, "r": 30},
            },
        
        }
        videos = get_youtube_videos(skill_name)

        # Convert video titles and URLs
        video_links = [
            html.Div([
                # Convert HTML entities in the title using html.unescape()
                html.A(
                    hyper.unescape(video['snippet']['title']),
                    href=f"https://www.youtube.com/watch?v={video['id']['videoId']}",
                    target="_blank",
                    className="text-blue-600 hover:text-blue-800 underline hover:underline font-bold"
                ),
                html.Br()  # Adds spacing between links
            ]) for video in videos
        ]

        # Display the skill description and the line chart
        return html.Div([
            html.H2(f'Skill Details: {skill_name.title()}'),
            html.P(description),  # Display description
            dcc.Graph(figure=individualSkill_over_time_fig),  # Deserialize and display the line chart using plotly.io
            html.H3("Related YouTube Courses", className="mt-8 text-lg font-semibold"),  # Section title for videos
            html.Div(video_links, className="pt-5 space-y-2")  # Display video links with some top padding and spacing between links
        ])



    # Show a 404 page if no valid route matches
    else:
        return html.Div([
            html.H2("404 - Page not found"),
            html.P("The page you are looking for does not exist.")
        ])


# Callback to handle bar click event and change the URL
@app.callback(
    Output('page-url', 'pathname'),  # Change the URL on click
    Input('top-skills-barchart', 'clickData')  # Input from clicking a bar
)
def on_bar_click(click_data):
    if click_data:  # When a bar is clicked
        clicked_skill = click_data['points'][0]['x']  # Get the clicked skill name
        # Redirect to a page related to that skill
        return f'/skills/{clicked_skill}'
    return '/'  # Default home page

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
