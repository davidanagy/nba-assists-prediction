import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Process

            ### Why NBA assists?

            I started following the NBA just last year, but I'm already addicted--though I admit that
            the storylines *around* the games are often more fun than the games themselves.
            In addition to my interest, there's a wealth of data about the NBA on the website
            [Basketball Reference][basketball-reference.com], which made it relatively
            straightforward to gather the data I needed for making predictions (more on that
            in a bit.) I was also curious--perhaps predicting assists might teach us some things,
            not only about basketball, but even about selfishness and altriusm.

            There were three main steps to getting the data necessary for this project: gather
            the data, manipulate it into a usable form, then construct and test models.

            """
        ),

    ],
)

column2 = dbc.Col(
    [html.Img(src='assets/picture1.jpg', className='img-fluid')]
)

layout = dbc.Row([column1, column2])