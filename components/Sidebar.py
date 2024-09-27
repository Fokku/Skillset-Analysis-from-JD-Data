from dash import html, dcc
from data.data import Data

data = Data()

def Sidebar():
    return html.Aside(
        className="px-10 h-full flex flex-row fixed inset-y-0 z-10 flex flex-shrink-0 w-[400px] max-h-screen overflow-hidden transition-all transform bg-white border-r shadow-lg lg:z-auto lg:static lg:shadow-none ",
        children=[
            html.Div(
                className="flex flex-col w-max h-full py-4 px-8 items-center gap-6 bg-[#FDFDFE]",
                children=[
                    html.Img(
                        className="mr-auto flex justify-center items-left h-[75px]",
                        src="https://i.ibb.co/R0MJZsp/sit-logo.png"),
                    Seperator(),
                    html.Div(
                        className="filter-options",
                        children=[
                            FilterGroup()
                        ]
                    )
                ]
            ),
        ]
    )

def Seperator(horizontal=True, className=None):
    return html.Div(
                className="{} self-stretch bg-gradient-to-tr from-transparent via-neutral-500 to-transparent opacity-25 dark:via-neutral color {}".format("w-full h-px min-w-full" if horizontal else "h-full w-px min-h-full", className if className else ""),
                )

def FilterGroup():
    return html.Div(
        className="flex flex-col gap-4",
        children=[
            html.P("Filter by Country:"),
            # Update dropdown options
            dcc.Dropdown(
                id = "country-filter",
                options=[{'label': country, 'value': country} for country in data.get_country_data()],
                value="US",
                clearable=False,
                multi=True
            ),
            html.P("Filter by Job Industries:"),
            dcc.Dropdown(
                options=[
                    {"label": "Software Development", "value": "Software Development"},
                    {"label": "Data Science", "value": "Data Science"},
                    {"label": "Product Management", "value": "Product Management"},
                    {"label": "Marketing", "value": "Marketing"},
                ],
                value="Software Development",
                clearable=False,
                multi=True
            )
        ]
    )