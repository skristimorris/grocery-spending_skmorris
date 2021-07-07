# app.py

import sqlite3 as sql
import dash
from dash_bootstrap_components._components.Collapse import Collapse
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_html_components.I import I
import plotly.express as px
import pandas as pd

# Ref: https://dash.plotly.com/layout
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# style attributes
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#f8f9fa'
}

CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'padding': '20px 10px'
}

# set this to 1 to recreate or overwrite the SQL with your hand edited csv file
if 0:
    df = pd.read_csv("data/expenses.csv") # read csv and set to dataframe df
    conn = sql.connect("data.db") # connect to sqlite and create database data.db
    df.to_sql("expenses", conn, if_exists = "replace", index = False) # insert dataframe into sql table called expenses
    conn.close()

conn = sql.connect("data.db")
df = pd.read_sql_query("SELECT category, SUM(price) AS price, strftime('%Y-%m', date) AS 'year-month' FROM expenses GROUP BY category, strftime('%Y-%m', date) ORDER BY strftime('%Y-%m', date), category", con=conn)
fig = px.bar(df, x="year-month", y="price", color="category", barmode="group")
print(df)
conn.close()

input_addItem = dbc.FormGroup(
    [
        html.P('Item Name', style={
            'textAlign': 'left'
        }),
        dcc.Input(
            id='name', 
            placeholder='Enter grocery item here...',
            style={'width': '100%'}
        ),
        html.Div(id='output-name'),
        html.Br(),
        html.P('Category', style={
            'textAlign': 'left'
        }),
        dcc.Dropdown(
            id='category',
            options=[{
                'label': 'Beverages',
                'value': 'beverages'
            }, {
                'label': 'Candy',
                'value': 'candy'
            }],
        ),
        html.Br(),
        html.P('Price', style={
            'textAlign': 'left'
        }),
        dcc.Input(
            id='price',
            type='number',
            placeholder='Enter grocery item price here...',
            style={'width': '100%'}
        ),
        html.Br(),
        html.Br(),
        html.P('Quantity', style={
            'textAlign': 'left'
        }),
        dcc.Slider(
            id='quantity',
            min=0,
            max=10,
            step=1,
            value=1,
            marks={
                0: '0',
                1: '1',
                2: '2',
                3: '3',
                4: '4',
                5:'5',
                6: '6',
                7: '7',
                8: '8',
                9: '9',
                10: '10'
            }
        ),
        html.Br(),
        html.P('Date', style={
            'textAlign': 'left'
        }),
        dcc.DatePickerSingle(
            id='date',
            month_format='MMM Do, YY'
        ),
        html.Br(),
        html.Br(),
        dbc.Button(
            id='submit_item',
            n_clicks=0,
            children='Submit',
            color='primary',
            block=True,
            style={'width': '40%'}
        )
    ]
)

# create add item collapse 
# Ref: https://dash-bootstrap-components.opensource.faculty.ai/docs/components/collapse/
collapse_addItem = html.Div(
    [
        dbc.Button(
            'Add Grocery Item',
            id='button-add-item',
            color='link',
            n_clicks=0,
        ),
        dbc.Collapse(
            dbc.CardBody(input_addItem),
            id='collapse-add-item',
            is_open=False,
        )
    ]
)

# create spending history collapse
collapse_spendHistory = html.Div(
    [
        dbc.Button(
            'Spending History',
            id='button-spending-history',
            color='link',
            n_clicks=0,
        ),
        dbc.Collapse(
            dbc.CardBody('content here'),
            id='collapse-spending-history',
            is_open=False,
        )
    ]
)

# create spending trends collapse
collapse_spendTrends = html.Div(
    [
        dbc.Button(
            'Spending Trends',
            id='button-spending-trends',
            color='link',
            n_clicks=0,
        ),
        dbc.Collapse(
            dbc.CardBody('content here'),
            id='collapse-spending-trends',
            is_open=False,
        )
    ]
)

# callback for add item collapse
@app.callback(
    Output('collapse-add-item', 'is_open'),
    [Input('button-add-item', 'n_clicks')],
    [State('collapse-add-item', 'is_open')],
)

def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# callback for spending history collapse
@app.callback(
    Output('collapse-spending-history', 'is_open'),
    [Input('button-spending-history', 'n_clicks')],
    [State('collapse-spending-history', 'is_open')],
)

def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# callback for spending trends collapse
@app.callback(
    Output('collapse-spending-trends', 'is_open'),
    [Input('button-spending-trends', 'n_clicks')],
    [State('collapse-spending-trends', 'is_open')],
)

def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# create sidebar attributes
sidebar = html.Div(
    [
    html.H4('Grocery Spending Tracker'),
    html.Hr(),
    collapse_addItem, # incorporate add item collapse
    collapse_spendHistory, # incorporate add spending history collapse
    collapse_spendTrends # incorporate add spending trends collapse
    ],
    style=SIDEBAR_STYLE
)

app.layout = html.Div([sidebar])

# create spending history collapse
collapse_spendHistory = html.Div(
    [
        dbc.Button(
            'Spending History',
            id='button-spending-history',
            color='link',
            n_clicks=0,
        ),
        dbc.Collapse(
            dbc.CardBody('content here'),
            id='collapse-spending-history',
            is_open=False,
        )
    ]
)
if __name__ == '__main__':
    app.run_server(debug=True)