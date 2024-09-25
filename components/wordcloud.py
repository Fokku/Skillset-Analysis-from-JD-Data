import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from wordcloud import WordCloud

# Sample data with more job programs
data = {
    'Programme': [
        'Information Security', 'AAI', 'Supply Chain', 
        'Data Science', 'Cyber Security', 'Software Engineering'
    ],
    'Job Positions': [120, 150, 100, 180, 130, 160],
    'Skills': [
        'Python, SQL', 'Machine Learning, AI', 'Logistics, Management', 
        'Python, Data Analysis', 'Security, Network', 'Programming, Debugging'
    ],
    'Average Salary': [70000, 80000, 75000, 85000, 78000, 83000],
    'Job Growth': [5, 7, 6, 8, 6, 7]
}
df = pd.DataFrame(data)

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app with a 2x2 grid layout for the graphs
app.layout = html.Div([
    dcc.Dropdown(
        id='programme-dropdown',
        options=[{'label': prog, 'value': prog} for prog in df['Programme']],
        value='Information Security',
        style={'width': '50%', 'margin-bottom': '20px'}
    ),
    html.Div([
        html.Div([dcc.Graph(id='skills-wordcloud')], className="graph-div"),
    ], className="row"),
], style={'display': 'flex', 'flex-direction': 'column'})

# Callback to update the word cloud based on dropdown selection
@app.callback(
    Output('skills-wordcloud', 'figure'),
    [Input('programme-dropdown', 'value')]
)
def update_wordcloud(selected_programme):
    filtered_df = df[df['Programme'] == selected_programme]
    text = filtered_df['Skills'].values[0]
    wordcloud = WordCloud().generate(text)
    
    fig = px.imshow(wordcloud, title=f'Skills for {selected_programme}')
    return fig

# CSS to style the graphs in a 2x2 layout
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=True)