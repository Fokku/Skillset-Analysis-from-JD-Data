from dash import html


def ProjectHeader():
    return (
        html.Div(
            className="flex flex-col items-start justify-between pb-6 space-y-4 border-b lg:items-center lg:space-y-0 lg:flex-row",
            children=[
                html.Div(
                    className="flex flex-col",
                    children=[
                        html.H1(
                            className="text-xl font-semibold text-slate-800",
                            children="INF1002 Programming Fundamentals - T3",
                        ),
                        html.H2(
                            className="text-lg font-default text-slate-600",
                            children="Data Analysis from Job Data",
                        ),
                    ],
                ),
                html.A(
                    href="test",
                    target="_blank",
                    children=[
                        html.A(
                            href="https://github.com/Fokku/Skillset-Analysis-from-JD-Data",
                            target="_blank",
                            children=[
                                html.Button(
                                    className="h-10 px-4 py-2 inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors outline-none focus-visible:ring-2 focus-within:ring-2 ring-ring ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground",
                                    children=[
                                        html.Span(
                                            className="font-semibold text-slate-800",
                                            children="View on GitHub",
                                        ),
                                    ],
                                )
                            ]
                        ),
                    ],
                ),
            ],
        ),
    )
