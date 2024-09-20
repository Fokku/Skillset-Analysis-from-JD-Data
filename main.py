import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, html, dcc, Input, Output, State
import requests
import json

app = Dash(__name__)

def main():
    app.layout = [html.Div([html.H1("Job Data API")])]
    app.run(debug=True)

if __name__ == "__main__":
    main()