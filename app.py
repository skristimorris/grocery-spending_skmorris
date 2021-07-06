# app.py

import sqlite3 as sql
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_html_components.I import I
import plotly.express as px
import pandas as pd

# Ref: https://dash.plotly.com/layout
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

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

'''
def generate_table(dataframe):
    return html.Table([html.Thead(html.Tr([html.Th(col) 
        for col in dataframe.columns])), html.Tbody([html.Tr([html.Td(dataframe.iloc[i][col]) 
        for col in dataframe.columns]) 
        for i in range(min(len(dataframe)))])])
'''
# Ref: https://dash.plotly.com/layout
#app.layout = html.Div(
#    children=[
#        html.H1(children='Hello Dash'),
#        html.Div(children='''Dash:  A web application framework for Python.'''),
#        dcc.Graph(
#            id='example-graph',
#            figure=fig
#        )
#    ]
#)

# Ref: https://dash-bootstrap-components.opensource.faculty.ai/docs/components/collapse/
app.layout = html.Div(
    [
        html.Div(html.H6('Grocery Spending Tracker')),
        html.Hr(),
        dbc.Button(
            'Add Grocery Item',
            color='link',
            id='add-item-button',
            n_clicks=0
            ),
        dbc.Collapse(
            dbc.CardBody('content here'),
            id='add-item-collapse',
            is_open=False
            ),
    ],
    style=SIDEBAR_STYLE
)

@app.callback(
    Output("add-item-collapse", "is_open"),
    [Input("add-item-button", "n_clicks")],
    [State("add-item-collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open




if __name__ == '__main__':
    app.run_server(debug=True)