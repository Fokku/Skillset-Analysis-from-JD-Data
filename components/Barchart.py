from dash import html, dcc


def BarChart(Title="Top 10 Skills", id="top-skills-barchart", description=None, figure=None, **kwargs) -> html.Div:
    if not figure:
        return html.Div(
            className="p-4 transition-shadow border rounded-lg shadow-sm hover:shadow-lg",
            children=[
                html.H1(
                    className="text-xl text-center font-semibold text-slate-800",
                    children=Title,
                ),
                html.P(
                    className="text-sm text-center text-slate-500",
                    children=description,
                ),
                dcc.Graph(
                    id=id, className="w-full h-[300px]", config={"displayModeBar": False}, **kwargs
                ),
            ],
        )
    else:
        return html.Div(
            className="p-4 transition-shadow border rounded-lg shadow-sm hover:shadow-lg",
            children=[
                dcc.Graph(
                    id=id,
                    className="w-full h-[300px]",
                    config={"displayModeBar": False},
                    figure=figure,
                    **kwargs,
                ),
                html.P(
                    className="text-sm text-center text-slate-500",
                    children=description,
                ),
            ],
        )
