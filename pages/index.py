import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

from app import app

"""
https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout

Layout in Bootstrap is controlled using the grid system. The Bootstrap grid has 
twelve columns.

There are three main layout components in dash-bootstrap-components: Container, 
Row, and Col.

The layout of your app should be built as a series of rows of columns.

We set md=4 indicating that on a 'medium' sized or larger screen each column 
should take up a third of the width. Since we don't specify behaviour on 
smaller size screens Bootstrap will allow the rows to wrap so as not to squash 
the content.
"""

column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Predict NBA assists!

            Who's your favorite NBA player? Is he a selfish scorer, only looking to pad his numbers? Or a willing distributor who wants all his teammates to succeed? Or...both!?

            Based on the prior performance of each player and his teammates, we can predict how many assists per game he'll have this year.

            Find out how selfish your player will be this season--and why!

            """
        ),
        dcc.Link(dbc.Button('Predict!', color='primary'), href='/predictions')
    ],
    md=4,
)

gapminder = px.data.gapminder()
fig = px.scatter(gapminder.query("year==2007"), x="gdpPercap", y="lifeExp", size="pop", color="continent",
           hover_name="country", log_x=True, size_max=60)

column2 = dbc.Col([html.Img(src='assets/front.jpg', className='img-fluid')])

layout = dbc.Row([column1, column2])