from dash import dcc, html

def Boxchart(id="none", Title=None, description="", figure=None):
    return html.Div(
        className="p-4 transition-shadow border rounded-lg shadow-sm hover:shadow-lg",
        children=[
            html.H1(
                className="text-xl text-center font-semibold text-slate-800",
                children=Title,
            ) if Title else None,
            dcc.Graph(
                id=id,
                figure=figure,
                className="w-full h-[300px]",
                config={"displayModeBar": False},
            ),
            html.P(
                className="text-sm text-center text-slate-500",
                children=description,
            ) if description else None,
        ]
    )