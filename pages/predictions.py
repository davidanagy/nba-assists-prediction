import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import category_encoders as ce
from sklearn.linear_model import Ridge

from app import app

test = pd.read_csv('csvs/final-predictions.csv')
train = pd.read_csv('csvs/training-data.csv')
X_train = train.drop(['Player', 'Tm', 'Target'], axis=1)
y_train = train['Target']
X_test = test.drop(['Player', 'Tm', 'preds'], axis=1)

encoder = ce.OneHotEncoder(use_cat_names=True)
X_train_encoded = encoder.fit_transform(X_train)
X_test_encoded = encoder.transform(X_test)

model = Ridge(alpha=431)
model.fit(X_train_encoded, y_train)
y_pred = model.predict(X_test_encoded)

test['preds'] = y_pred
test2 = X_test_encoded.copy()
test2['Player'] = test['Player']

options = []
for i in range(len(test)):
    d = {}
    d['label'] = test.loc[i, 'Player']
    d['value'] = test.loc[i, 'Player']
    options.append(d)

column1 = dbc.Col(
    [
        dcc.Markdown('## Choose a player!', className='mb-5'),
        dcc.Dropdown(id='player', value='LeBron James', options=options),
        dbc.Button('Predict!', id='button', n_clicks=1, color='primary',
                  style=dict(marginTop=1.75, marginBottom=10))
    ],
    md=4,
)

column2 = dbc.Col(
    [
        html.H2('Prediction:', className='mb-5'),
        html.Div(id='assists')
    ]
)

row1 = dbc.Row([column1, column2])

row2 = dbc.Row(
    [
        html.H2('Major stats:', className='mb-5'),
        html.Div(id='imp_stats')
    ]
)

@app.callback(
    [Output('assists', 'children')],
    [Input('button', 'n_clicks')],
    [State('player', 'value')]
)
def predict(clicked, name):
    if clicked:
        for i in range(len(test)):
            if test.loc[i, 'Player'] == name:
                assist_pred = test.loc[i, 'preds']
                return [assist_pred]
                break

layout = dbc.Row([column1, column2])