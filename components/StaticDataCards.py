from dash import html, dcc


def StaticDataCards(title="Title", value="Value", id="id"):
    return html.Div(
        className="p-6 transition-shadow border rounded-lg shadow-sm hover:shadow-lg",
        children=[
            html.Div(
                className="flex flex-row items-start justify-between",
                children=[
                    html.Div(
                        className="flex flex-col space-y-2",
                        children=[
                            html.Span(
                                className="text-lg text-slate-400", children=title
                            ),
                            html.Span(
                                id=f"{id}-value",
                                className="text-xl font-semibold text-slate-800",
                                children=value,
                            ),
                        ],
                    ),
                    html.Div(
                        className="bg-slate-200 rounded-md",
                        children=[
                            dcc.Graph(
                                id=id,
                                className="w-24 h-24",
                                config={"displayModeBar": False},
                            )
                        ],
                    ),
                ],
            ),
        ],
    )
