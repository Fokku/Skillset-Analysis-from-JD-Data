from dash import dcc, html
import plotly.express as px

# Pie charts will account for representing 4 types of data (filtered by values from the filters):
# Total jobs
# Total companies
# Total job industries
# Total job skills

def Piechart(data):
    fig = px.pie(data, values='total_bill', names='day')
    return html.Div([
        dcc.Graph(
            id='piechart',
            figure=fig
        )
    ])