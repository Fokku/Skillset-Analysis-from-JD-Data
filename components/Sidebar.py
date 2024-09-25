from dash import html, dcc

def Sidebar():
    return html.Div(
        className="flex flex-row",
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
            Seperator(horizontal=False),
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
                options=[
                    {"label": "United States", "value": "US"},
                    {"label": "Canada", "value": "CA"},
                    {"label": "United Kingdom", "value": "UK"},
                    {"label": "Australia", "value": "AU"},
                ],
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