import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

from app import app

df = pd.read_csv('assist-predictions.csv')

options = []
for i in range(len(df)):
    d = {}
    d['label'] = df.loc[i, 'Player']
    d['value'] = df.loc[i, 'Player']
    options.append(d)

column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Predictions


            """
        ),
        dcc.Dropdown(options=options)
    ],
    md=4,
)

column2 = dbc.Col(
    [
        
    ]
)

layout = dbc.Row([column1, column2])