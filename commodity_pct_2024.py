import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Load the data
cmo_df = pd.read_csv("CMO-Historical-Data-Monthly.csv")

# Drop sub headers
cmo_df = cmo_df.drop([0, 1])

# Rename the first column to 'Date'
cmo_df.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)

# Convert 'Date' column to datetime format
cmo_df['Date'] = pd.to_datetime(cmo_df['Date'], format='%YM%m')

# Convert all other columns to numeric, coercing errors to NaN
cmo_df.iloc[:, 1:] = cmo_df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')

# Filter data from 2020 onwards and calculate percentage change
cmo_2020_2024_df = (cmo_df.query("Date >= '2020-01-01'").set_index('Date').pct_change(fill_method=None) * 100).round(2)


# Initialize the Dash app with a Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SIMPLEX])

## Title
app.title = "Comodities Percentage Change"

# Define the layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H3("Commodity Percentage Changes (2020-2024)"),style={'text-align': 'center', 'margin': '10px','padding': '10px'}, width=12)
    ]),
    dbc.Row([
        dbc.Col(
        dbc.RadioItems(
            id='resample-frequency',
            options=[
                {'label': 'Monthly', 'value': 'ME'},
                {'label': 'Quarterly', 'value': 'QE'},
                {'label': 'Yearly', 'value': 'YE'}
            ],
            value='ME',
            inline=True,
            style={'text-align': 'left', 'padding': '10px'}
            
            
        )
               )
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='commodity-dropdown',
                options=[{'label': col, 'value': col} for col in cmo_2020_2024_df.columns],
                placeholder="Select a Comodities",
                value=['Crude oil, WTI', 'Coffee, Arabica', 'Gold', 'Palm kernel oil'],
                multi=True,
                className='card border-primary mb-3',
                style={'text-align': 'left', 'padding': '10px'},
            
            
        ), width=5),
        dbc.Tooltip("Select a Commodity from the dropdown menu.", target="commodity-dropdown",
                   placement="top", style={'fontSize': '16px', 'borderRadius': '5px', 'padding': '10px'}
                   
                   
                   
                   ),
       
   
    ]),
    dbc.Row([
        dbc.Col(html.H4("Monitoring the Fluctuations in Commodity Prices Through Comparative Percentage Analysis"),
                style={'text-align': 'center', 'margin': '10px','padding': '10px'}, width=12)
    ]),
    # html.Hr(),
    
    dbc.Row([
        dbc.Col(dbc.Card(
            dbc.CardBody([
                dcc.Graph(id='scatter-plot')
            ]),
        className='card border-light mb-3'), width=12)
    ])
], fluid=True
                          )

# Define callback to update graph
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('commodity-dropdown', 'value'),
     Input('resample-frequency', 'value')]
)
def update_graph(selected_commodities, resample_freq):
    # Resample data based on selected frequency
    resampled_data = cmo_2020_2024_df.resample(resample_freq).mean()
    
    fig = px.scatter(resampled_data, 
                     x=resampled_data.index, 
                     y=selected_commodities,
                     template='xgridoff', 
                     marginal_y='violin',
                     labels={'value': 'Percentage Change', 'variable': 'Commodities', 'Date':''},
                     )
    
    fig.update_traces(marker=dict(size=15))

    fig.update_layout(
        legend=dict(title=None,orientation="h", y=1.3, 
                    yanchor="top", x=0.5, xanchor="center", font=dict(size=20)),
        xaxis=dict(showline=True, showgrid=True, showticklabels=True,
                   linecolor='rgb(199, 199, 199)', linewidth=0.5,
                   ticks='inside', tickfont=dict(family='Arial', size=16, color='rgb(82, 82, 82)'),
                   
            ),
        yaxis=dict(showline=True, showgrid=True, showticklabels=True,
                   linecolor='rgb(199, 199, 199)', linewidth=0.5,
                   ticks='inside', tickfont=dict(family='Arial', size=16, color='rgb(82, 82, 82)'),
                   zeroline=True, zerolinecolor='#c7c8c9'
                  
                  )
                                 
                )
    
    # fig.update_xaxes(nticks=10)



    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True,jupyter_mode='external', port=8070)
