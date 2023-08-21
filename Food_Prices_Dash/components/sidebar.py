import os
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app

from datetime import datetime, date
import plotly.express as px
import numpy as np
import pandas as pd

from dash import Dash, html, dcc, Input, Output
import pandas as pd


# =========Layout ========= #

layout = dbc.Col([
    
    # Sidebar Title
    html.H1('Food Prices',className='text-primary text-center'),
    html.Hr(),
    
    # Sidebar Image
    html.Img(src=app.get_asset_url("Food_Prices.png"), alt="Food Image", className="img-fluid mx-auto",style={'width': '90%'}),
    
    # Dashboard Description
       # Text description
    html.P(
        "This interactive dashboard utilizes Global Food Prices data from the World Food Programme, from more than 76 countries and nearly 1,500 markets. The dataset presents data from 1992 for a few nations, while many countries started reporting from 2003 or later.", 
        style={"text-align": "justify","padding": "15px"}
    ),
    html.P(
        "The primary objective of this dashboard is to analyze and present trends in food prices based on various factors, including food category, market type, city, country, and year. By visualizing and exploring this data, we aim to gain insights into the fluctuations and patterns of food prices across different regions and periods.",
        style={"text-align": "justify","padding": "15px"}
    )
    
])

