# dashboard.py

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import dash_table

df = pd.read_csv("data/expenses.csv")

CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'padding': '20px 10px'
}

# create form with inputs to filter dashboard
def InputDashboard():
    input_dashboard = dbc.FormGroup(
        [
            html.P('Item Name', style={
                'textAlign': 'left'
            }),
            dcc.Dropdown(
                id='dash-name',
                options=[
                    {'label': i, 'value': i} for i in sorted(df.name.unique())
                ],
                multi=True,
            ),
            html.Div(id='output-dash-name'),
            html.Br(),
            html.P('Category', style={
                'textAlign': 'left'
            }),
            dcc.Dropdown(
                id='dash-category',
                options=[
                    {'label': i, 'value': i} for i in sorted(df.category.unique())
                ],
                multi=True,
            ),
            html.Div(id='output-dash-category'),
            html.Br(),
            html.P('Date', style={
                'textAlign': 'left'
            }),
            dcc.DatePickerSingle(
                id='dash-date',
                month_format='MMM Do, YY'
            ),
            html.Br(),
            html.Br(),
            html.Div(id='output-dash-date'),
            dbc.Button(
                id='submit_dash',
                n_clicks=0,
                children='Submit',
                color='primary',
                block=True,
                style={'width': '40%'}
            )
        ]
    )
    return input_dashboard

# Ref: https://dash-bootstrap-components.opensource.faculty.ai/docs/components/collapse/
# create dashboard collapse 
def CollapseDashboard():
    collapse_dashboard = html.Div(
        [
            dbc.Nav(
                [
                    dbc.NavLink(
                    'Dashboard',
                    href='/dashboard',
                    id='button-dashboard',
                    active='exact',
                    n_clicks=0,
                ),
                ],
            ),
            dbc.Collapse(
                dbc.CardBody(InputDashboard()),
                id='collapse-dashboard',
                is_open=True,
            )
        ]
    )
    return collapse_dashboard

# create graphs for dashboard
def GenerateGraphs():
    generate_graphs = html.Div(
        [
            html.Br(),
            html.Br(),
            html.H5('Dashboard'),
            html.Hr(),
            dbc.Col(dcc.Graph(
                id='graph_1',
                figure = px.bar(df, x="date", y="price", color="category", barmode="group"),
            )
            )
        ]
    )
    return generate_graphs

# create dashboard layout
layout = html.Div(
    [
    html.Br(),
    html.Br(),
    GenerateGraphs()
    ],
    style=CONTENT_STYLE
)