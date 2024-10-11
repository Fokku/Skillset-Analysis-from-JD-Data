from dash import html, dcc
from data.data import Data

data = Data()


def MultiLineChart(Title="Skillset Requirements Over Time"):
    return html.Div(
        className="p-4 transition-shadow border rounded-lg shadow-sm hover:shadow-lg",
        children=[
            html.H1(
                className="text-xl text-center font-semibold text-slate-800",
                children=Title,
            ),
            dcc.Graph(
                id="skills-over-time-chart",
                className="w-full h-[300px]",
                config={"displayModeBar": False},
            ),
        ],
    )


def InteractiveMultiLineChart(Title="Skillset Requirements Over Time", id="interactive-skills-over-time-chart"):
    return html.Div(
        className="col-span-2 p-4 transition-shadow border rounded-lg shadow-sm hover:shadow-lg",
        children=[
            html.H1(
                className="text-xl text-center font-semibold text-slate-800",
                children=Title,
            ),
            html.Div(
                className="w-full justify-start",
                children=[
                    dcc.Dropdown(
                        id="skill-filter",
                        className="flex h-10 w-[200px] items-center justify-between rounded-md border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 [&>span]:line-clamp-1",
                        options=[
                            {"label": skill, "value": skill}
                            for skill in data.get_skills_list()
                            if type(skill) == str
                        ],
                        placeholder="Select skills",
                        multi=True,
                    )
                ],
            ),
            dcc.Graph(
                id=id,
                className="w-full h-[300px]",
                config={"displayModeBar": False},
                animate=True,
            ),
        ],
    )
