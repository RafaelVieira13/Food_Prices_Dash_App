from dash import html, dcc
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from app import *
from components import sidebar, dashboards

#=========  Layout  =========== #
content = html.Div(id="page-content")


app.layout = dbc.Container(children=[
    dbc.Row([
        dbc.Col([
            dcc.Location(id='url'),
            sidebar.layout
        ], md=2),
        dbc.Col([
            dashboards.layout
        ], md=10)
    ])

], fluid=True)


if __name__ == '__main__':
    app.run_server(port=8051, debug=True)