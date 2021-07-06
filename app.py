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
            dbc.CardBody('content here'),
            id='collapse-add-item',
            is_open=False,
        )
    ]
)

@app.callback(
    Output('collapse-add-item', 'is_open'),
    [Input('button-add-item', 'n_clicks')],
    [State('collapse-add-item', 'is_open')],
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
    collapse_addItem # incorporate add item collapse
    ],
    style=SIDEBAR_STYLE
)

app.layout = html.Div([sidebar])

if __name__ == '__main__':
    app.run_server(debug=True)