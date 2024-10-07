from dash import html, dcc
from data.data import Data
from components.Seperator import Seperator
from dash_daq import BooleanSwitch

data = Data()


def Sidebar():
    return html.Aside(
        id="sidebar",
        className="px-4 h-full flex flex-row fixed inset-y-0 z-10 flex flex-shrink-0 w-[300px] max-h-screen overflow-hidden transition-all transform bg-white border-r shadow-lg lg:z-auto lg:static lg:shadow-none items-center",
        children=[
            html.Div(
                className="flex flex-col w-full h-full py-4 px-4 items-center gap-6 bg-[#FDFDFE]",
                children=[
                    html.Img(
                        className="mx-auto flex justify-center items-left h-[75px]",
                        src="https://i.ibb.co/R0MJZsp/sit-logo.png",
                    ),
                    Seperator(),
                    html.Div(className="filter-options", children=[FilterGroup()]),
                    #Button that hovers in the vertical center of the sidebar, lingering over the edge of the side. It will be used to toggle the sidebar
                    # html.Button(
                    #     className="ml-[120%] z-20 size-10 bg-black text-white rounded-full flex items-center justify-center",
                    #     children="<",
                    #     id="toggle-sidebar-button",
                    # ),
                ],
            ),
        ],
    )


def ToggleSwitch():
    return (
        dcc.Checklist(
            inputClassName="sr-only peer",
            labelClassName="inline-flex items-center cursor-pointer",
            id="general-view-toggle",
            options=[
                {
                    "label": html.Div(
                        className="relative w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"
                    ),
                    "value": False,
                }
            ],
        ),
    )


def FilterGroup():
    return html.Div(
        className="w-full flex flex-col gap-4",
        children=[
            html.P("Filter by Country:"),
            # Update dropdown options
            dcc.Dropdown(
                className="flex h-10 w-full items-center justify-between rounded-md border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 [&>span]:line-clamp-1",
                id="country-filter",
                options=[
                    {"label": country, "value": country}
                    for country in data.get_country_list()
                ],
                optionHeight=30,
                multi=True,  # Set to False if you want only single selection
                placeholder="Select countries",
            ),
            html.P("Filter by Job Industries:"),
            dcc.Dropdown(
                className="flex h-10 w-full items-center justify-between rounded-md border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 [&>span]:line-clamp-1",
                id="industry-filter",
                options=[
                    {"label": industry, "value": industry}
                    for industry in data.get_industry_list()
                ],
                optionHeight=50,
                multi=True,  # Set to False if you want only single selection
                placeholder="Select industries",
            ),
            html.P("Toggle general view"),
            ToggleSwitch()[0],
        ],
    )
