# app.py

import sqlite3 as sql
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

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
app.layout = html.Div(children=[html.H1(children='Hello Dash'), html.Div(children='''Dash:  A web applciation framework for Python.'''), dcc.Graph(id='example-graph', figure=fig)])

#app.layout = html.Div(children=[html.H4(children='Table'), generate_table(df)])

if __name__ == '__main__':
    app.run_server(debug=True)