from dash import dcc, html

# Pie charts will account for representing 4 types of data (filtered by values from the filters):
# Total jobs
# Total companies
# Total job industries
# Total job skills
# Distribution of Remote vs Onsite positions

def Piechart(Title="", id="", figure=None, **kwargs) -> html.Div:
    if not figure:
        return html.Div(
            className="p-4 transition-shadow border rounded-lg shadow-sm hover:shadow-lg",
            children=[
                html.H1(
                    className="text-xl text-center font-semibold text-slate-800",
                    children=Title,
                ),
                dcc.Graph(
                    id=id, className="w-full h-[300px]", config={"displayModeBar": False}, **kwargs
                ),
            ],
        )
    else:
        return html.Div(
            className="p-4 transition-shadow border rounded-lg shadow-sm hover:shadow-lg",
            children=dcc.Graph(
                id=id,
                className="w-full h-[300px]",
                config={"displayModeBar": False},
                figure=figure,
                **kwargs,
            ),
        )