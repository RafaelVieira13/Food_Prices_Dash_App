from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from app import app

# ========== Styles ============ #
tab_card = {'height': '100%'}

main_config = {
    "hovermode": "x unified",
    "legend": {
        "yanchor": "top",
        "y": 0.9,
        "xanchor": "left",
        "x": 0.1,
        "title": {"text": None},
        "font": {"color": "white"},
        "bgcolor": "rgba(0,0,0,0.5)"
    },
    "margin": {"l": 10, "r": 10, "t": 10, "b": 10}
}

config_graph = {"displayModeBar": False, "showTips": False}

card_icon = {
    'color': 'white',
    'textAlign': 'center',
    'fontSize': 30,
    'margin': 'auto'
}

# Indicators Height
indicator_height = 200

# =========  Reading The Data  =========== #
df = pd.read_csv('data_clean.csv', low_memory=False)

# =========  Functions To Filter the Data  =========== #

# Country
def country_filter(selected_country):
    country_mask = df['Country'].isin([selected_country])
    return country_mask

# Years
def filter_years(selected_years):
    filtered_df = df[(df['Year'] >= selected_years[0]) & (df['Year'] <= selected_years[1])]
    return filtered_df

# Create the layout
layout = dbc.Col([
    # Row 1 -- Country Filter
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.Legend('Select a Country', className='card-title'),
                html.Div(
                    dcc.Dropdown(
                        id='dropdown_country',
                        options=[{'label': country, 'value': country} for country in df['Country'].unique()],
                        value=df.groupby('Country')['Price (EUR/kg)'].mean().idxmax(),
                        persistence=True,
                        persistence_type='session'
                    )
                )
            ], style={'margin': '15px'})
        ])
    ]),

    # Row 2 -- Indicators
    dbc.Row([
        dbc.Col([
            dbc.CardGroup([
                dbc.Card(
                    dcc.Graph(id='indicator_country', className='dbc'),
                    style={'padding-left': '20px', 'padding-top': '5px'}
                ),
                dbc.Card(
                    html.Div(html.I(className='fa fa-globe'), style=card_icon),
                    color='lightsteelblue',
                    style={'maxWidth': '65px', 'height': indicator_height, 'margin-left': '-10px'}
                )
            ])
        ], width=4),
        dbc.Col([
            dbc.CardGroup([
                dbc.Card(
                    dcc.Graph(id='city_indicator', className='dbc'),
                    style={'padding-left': '20px', 'padding-top': '5px'}
                ),
                dbc.Card(
                    html.Div(html.I(className='fa fa-globe'), style=card_icon),
                    color='lightsteelblue',
                    style={'maxWidth': '65px', 'height': indicator_height, 'margin-left': '-10px'}
                )
            ])
        ], width=4),
        dbc.Col([
            dbc.CardGroup([
                dbc.Card(
                    dcc.Graph(id='food_category', className='dbc'),
                    style={'padding-left': '20px', 'padding-top': '5px'}
                ),
                dbc.Card(
                    html.Div(html.I(className='fa fa-cutlery'), style=card_icon),
                    color='lightsteelblue',
                    style={'maxWidth': '65px', 'height': indicator_height, 'margin-left': '-10px'}
                )
            ])
        ], width=4)
    ], style={'margin': '15px'}),

    # Row 3 --- Market Type, Product Categories Prices
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dcc.Graph(id='market_type'),style={'height':'100%','padding':'10px'}
            ),width=6
        ),
        dbc.Col(
            dbc.Card(
                dcc.Graph(id='product_category',style={'height':'100%','padding':'10px'})
            ),width=6
        )
    ],style={'margin':'15px'}),
    
    # Row 3 ---- Year Prices
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dcc.Graph(id='year_prices',style={'height':'100%','padding':'10px'})
            ),width=12
        )
    ],style={'margin':'10px'}),
    
    # Row 4 ---- Year Slider
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Choose a Year Range",style={'font-size': '15px', 'padding': '0.5rem'}), 
                dbc.CardBody(
                    dcc.RangeSlider(
                        id='year_slider',
                        min=df['Year'].min(),
                        max=df['Year'].max(),
                        step=1,
                        marks={str(year): str(year) for year in range(df['Year'].min(), df['Year'].max() + 1)},
                        value=[df['Year'].min(), df['Year'].max()]
                    )
                )
            ]),
            style={'margin': '10px'}
        )
])

])


# =========  Callbacks  =========== #
@app.callback(
    [Output('indicator_country', 'figure'),
     Output('city_indicator', 'figure'),
     Output('food_category', 'figure')],
    [Input('dropdown_country', 'value')]
)
def indicators(selected_country):
    country_mask = country_filter(selected_country)
    df_filtered = df.loc[country_mask]

    # Indicator Country
    df1 = df_filtered.groupby('Country')['Price (EUR/kg)'].mean().reset_index().sort_values(by='Price (EUR/kg)', ascending=False)
    if not df1.empty:
        indicator_country = go.Figure(go.Indicator(
            mode='number',
            title=f"<span style='font-size:120%'>{df1['Country'].iloc[0]}<br><span style='font-size:70%'>Average Food Prices</span><br>",
            value=df1['Price (EUR/kg)'].iloc[0],
            number={'suffix': "€/kg",'font':{'size':60}}))
    else:
        indicator_country = go.Figure(go.Indicator(title='Country'))
        indicator_country.add_annotation(
        text="No data available",
        x=0.5,
        y=0.5,
        showarrow=False,
        font={'size': 16})

    # Indicator Food Product
    df2 = df_filtered.groupby('Product Category')['Price (EUR/kg)'].mean().reset_index().sort_values(by='Price (EUR/kg)', ascending=False)
    if not df2.empty:
        indicator_product_categ = go.Figure(go.Indicator(
            mode='number+delta',
            title=f"<span style='font-size:120%'>{df2['Product Category'].iloc[0]} - Expensive Food Category</span><br><span style='font-size:70%'>Compared To The Average Price of All Products Categories</span><br>",
            value=df2['Price (EUR/kg)'].iloc[0],
            number={'suffix': "€/kg",'font':{'size':60}},
            delta={'relative': True, 'valueformat': '.1%', 'reference': df2['Price (EUR/kg)'].mean()}))
    else:
        indicator_product_categ = go.Figure(go.Indicator(title='Product Category'))
        indicator_product_categ.add_annotation(
        text="No data available",
        x=0.5,
        y=0.5,
        showarrow=False,
        font={'size': 16})
        
   # Indicator City
    df3 = df_filtered.groupby('City')['Price (EUR/kg)'].mean().reset_index().sort_values(by='Price (EUR/kg)', ascending=False)
    if not df3.empty:
        indicator_city = go.Figure(go.Indicator(
            mode='number+delta',
            title=f"<span style='font-size:120%'>{df3['City'].iloc[0]} - Expensive City</span><br><span style='font-size:70%'>Average Food Prices Compared to Others Cities</span><br>",
            value=df3['Price (EUR/kg)'].iloc[0],
            number={'suffix': "€/kg",'font':{'size':60}},
            delta={'relative': True, 'valueformat': '.1%', 'reference': df3['Price (EUR/kg)'].mean()}))

    else:
        indicator_city = go.Figure(go.Indicator(title='City'))
        
    # Change the Layout
    indicator_country.update_layout(main_config, height=indicator_height)
    indicator_product_categ.update_layout(main_config, height=indicator_height)
    indicator_city.update_layout(main_config, height=indicator_height)

    return indicator_country, indicator_city, indicator_product_categ

# Market Type - Prices
@app.callback(Output('market_type','figure'),
    [Input('dropdown_country', 'value')]
)
def market_type(selected_country):
    country_mask = country_filter(selected_country)
    df_filtered = df.loc[country_mask]
    
    df4 = df_filtered.groupby('Market Type')['Price (EUR/kg)'].mean().reset_index().sort_values(by='Price (EUR/kg)',ascending=False)
    market_type = go.Figure(go.Bar(
        x=df4['Market Type'],
        y=df4['Price (EUR/kg)'],
        orientation='v',
        textposition='auto',
        text=[f'{round(price, 1)} EUR/kg' for price in df4['Price (EUR/kg)']],
        insidetextfont=dict(family='Times', size=20)))
    
    market_type.update_layout(title_text="Food Prices By Market", 
                                   title_font=dict(family='Arial', size=30),
                                   title_x=0.5,
                                   title_y=0.95)
    
    return market_type

# Product Category - Prices
@app.callback(Output('product_category', 'figure'),
              [Input('dropdown_country', 'value')])
def product_category(selected_country):  # Fixed function name typo here
    country_mask = country_filter(selected_country)
    df_filtered = df.loc[country_mask]

    df5 = df_filtered.groupby('Product Category')['Price (EUR/kg)'].mean().reset_index().sort_values(by='Price (EUR/kg)', ascending=False).head(10)
    df5.sort_values(by='Price (EUR/kg)', ascending=True, inplace=True)
    product_category = go.Figure(go.Bar(
        y=df5['Product Category'],
        x=df5['Price (EUR/kg)'],
        orientation='h',
        textposition='auto',
        text=[f'{round(price, 1)} EUR/kg' for price in df5['Price (EUR/kg)']],
        insidetextfont=dict(family='Times', size=24)))

    product_category.update_yaxes(title_text='', tickfont=dict(size=18))
    product_category.update_xaxes(tickvals=[])

    product_category.update_layout(title_text="Product Prices by Category (Top 10)",
                                   title_font=dict(family='Arial', size=30),
                                   title_x=0.5,
                                   title_y=0.95)

    return product_category

# Food Prices By Year
@app.callback(Output('year_prices', 'figure'),
              [Input('year_slider', 'value')])
def food_prices_year(selected_years):
    year_df_filtered = filter_years(selected_years)  # Filter the DataFrame

    df6 = year_df_filtered.groupby('Year')['Price (EUR/kg)'].mean().reset_index()

    by_year = go.Figure(go.Scatter(
        x=df6['Year'],
        y=df6['Price (EUR/kg)'],
        mode='lines',
        fill='tonexty',
        hovertemplate='Year: %{x}<br>Average Price: %{y:.2f} EUR/kg'))  # Fixed hovertemplate typo here

    by_year.update_layout(
        title_text='Food Prices by Year - All Countries',
        title_font=dict(family='Arial', size=30),
        title_x=0.5,
        title_y=0.95,
        xaxis_title='Year',
        yaxis_title='Price (EUR/kg)',
        xaxis_tickmode='linear',  # To show all years on x-axis
        xaxis_dtick=1,
        yaxis_dtick=0.2)

    return by_year
    