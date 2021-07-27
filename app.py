# app.py

from __future__ import annotations
import dash
import dash_core_components as dcc
from dash_core_components.Graph import Graph
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from pandas.io.formats import style
import plotly.express as px
import pandas as pd
import dash_table
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import numpy as np
from datetime import date

# set dataframe
df = pd.read_csv('data/items.csv')

# add 'total' column to df
df['total'] = df['price'] * df['quantity']

# add 'month_year' column to df that assigns month & year to each item based on purchase date
df['month_year'] = pd.to_datetime(df['date']).dt.strftime('%B %Y')
print(df)

# group df by month_year and category - am i using this?
df_group = df.groupby(['month_year', 'category']).sum().sort_values(by=['month_year'], ascending=False)
print(df_group)

# df for table
df_table = df[['name', 'price', 'quantity', 'total', 'date']]
print(df_table)

# create variable for current date in format of month & year to assign as default value for date dropdown
today = date.today()
current_MY = today.strftime('%B %Y')


# Ref: https://dash.plotly.com/layout
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True

# Ref: https://dash-bootstrap-components.opensource.faculty.ai/docs/components/form/
# create form with inputs to add new item
def InputItem():
    input_addItem = dbc.FormGroup(
        [
            html.P('Item Name', style={
                'textAlign': 'left'
            }),
            dcc.Input(
                id='name', 
                placeholder='Enter grocery item',
                style={'width': '100%'}
            ),
            html.Div(id='output-name'),
            html.Br(),
            html.P('Category', style={
                'textAlign': 'left'
            }),
            dcc.Dropdown(
                id='category',
                options=[
                    {'label': i, 'value': i} for i in sorted(df.category.unique())
                ],
            ),
            html.Div(id='output-category'),
            html.Br(),
            html.P('Price', style={
                'textAlign': 'left'
            }),
            dcc.Input(
                id='price',
                type='number',
                placeholder='Enter price of item',
                style={'width': '100%'}
            ),
            html.Div(id='output-price'),
            html.Br(),
            html.P('Quantity', style={
                'textAlign': 'left'
            }),
            dcc.Slider(
                id='quantity',
                min=0,
                max=10,
                step=1,
                #value=1,
                marks={
                i: '{}'.format(i)
                if i == 1
                else str(i)
                for i in range(1,11)
                },
                value=1,
            ),
            html.Div(id='output-quantity'),
            html.Br(),
            html.P('Date', style={
                'textAlign': 'left'
            }),
            dcc.DatePickerSingle(
                id='date',
                month_format='MMM Do, YY'
            ),
            html.Div(id='output-date'),
            html.Br(),
            html.Br(),
            html.Div(id='output-input-form')
        ]
    )
    return input_addItem

# create button to add new item and submit and close modal
button_item = html.Div([
dbc.Row(
    [
        dbc.Col(
            dbc.Button(
                "New Item", id='button-new-item', color="primary", className="ml-2", n_clicks=0, block=True
            ),
            width="auto",
            
        ),
        dbc.Modal(
        [
        dbc.ModalHeader('Add New Item'),
        dbc.ModalBody(InputItem()),
        dbc.ModalFooter(
            [
            dbc.Button('Submit', id='submit-new-item', className='ml-auto', n_clicks=0, color='primary'),
            dbc.Button('Close', id='close', className='ml-auto', n_clicks=0, color='primary')
            ]
        )
        ],
        id='modal',
        is_open=False,
    )
    ],
    no_gutters=True,
    className="ml-auto flex-nowrap mt-3 mt-md-0",
    align="center"
),
])

# work on this = graph layout
# Ref: https://dash.plotly.com/dash-core-components/graph
# create graph layout
dashboard = html.Div(
        [
            html.Br(),
            html.Br(),
            html.H5('Spending Dashboard', style={'textAlign': 'left'}),
            html.Hr(),
            html.Div([
                dcc.Dropdown(
                    id='dash-monthyear',
                    options=[
                        {'label': i, 'value': i} for i in sorted(df.month_year.unique())
                    ],
                    value=current_MY,
                )],
                style={
                    'width': '20%',
                    'display': 'inline-block'
                },
            ),
            dbc.Row(
                dcc.Graph(id='graph-spending-all')
                ),
            html.Hr(),
            html.Div([
                dcc.Dropdown(id='dash-category',)
            ],
                style={
                    'width': '20%',
                    'display': 'inline-block'
                },
            ),
            html.Br(),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(id='graph-item')
                ),
                dbc.Col(
                    dash_table.DataTable(
                        id='table-spending-category',
                        data=df.to_dict('records'),
                        columns=[
                            {
                            'name': i, 'id': i
                            }
                            for i in (df_table.columns)
                            ],
                        filter_action='native',
                        page_action='native',
                        page_current=0,
                        page_size=10,
                        sort_action='native',
                        sort_mode='single',
                        sort_by=[{'column_id': 'date', 'direction': 'desc'}],
                        style_cell={'textAlign': 'left'},
                        selected_columns=[],
                        selected_rows=[],
                        style_as_list_view=True,
                        )
                )
            ]),
            dbc.Row(
                    dcc.Graph(id='graph-trend')
                ),
        ],
        style={
            'margin-left': '25%',
            'margin-right': '5%',
            'padding': '20px 10px'
        }
)

# Ref: https://dash-bootstrap-components.opensource.faculty.ai/docs/components/navbar/#
navbar = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("Grocery Spending Tracker", className="ml-2")),
                ],
                align="left",
                no_gutters=True,
            ),
        ),
    ],
    color="dark",
    dark=True,
    fixed='top'
)

# Ref: https://dash-bootstrap-components.opensource.faculty.ai/examples/simple-sidebar/
# create sidebar
sidebar = html.Div(
    [
    html.Br(),
    html.Br(),
    #html.H5('Filter Criteria', style={'textAlign': 'left'}),
    #html.Hr(),
    button_item,
    ],
    style={
        'position': 'fixed',
        'top': 0,
        'left': 0,
        'bottom': 0,
        'width': '20%',
        'padding': '20px 10px',
        'background-color': '#f8f9fa'
    }
)

# Ref: https://dash.plotly.com/basic-callbacks
# callback to set category dropdown options based on month selected - not selecting cat for month
@app.callback(
    Output('dash-category', 'options'),
    [Input('dash-monthyear', 'value')]
)
def set_cat_option(month_year):
    df_cat = df.query('month_year == @month_year')
    return [{'label': i, 'value': i} for i in df_cat.category.unique()]

# callback to set category dropdown default value
@app.callback(
    Output('dash-category', 'value'),
    [Input('dash-category', 'options')]
)
def set_cat_default(available_options):
    return available_options[0]['value']

# Ref: https://plotly.com/python/pie-charts/
# callback to display graph for all categories
@app.callback(
    Output('graph-spending-all', 'figure'),
    [Input('dash-monthyear', 'value')]
)
def update_graph_spending_all(month_year):
    fig = px.pie(df.query('month_year == @month_year'), 
        values='total', 
        names='category', 
        title= 'Spending for All Categories in {}'.format(month_year),
        hole= .5,
    )
    fig.update_traces(
        hoverinfo='label+percent', 
        #text=['$' + total for total in fig.total.values],
        textinfo='value'
    )
    fig.update_layout(
        annotations= [
            dict(text= 'Total Amount <br> $', x=0.5, y=0.5, font_size=15, showarrow=False),
            ],
            legend_title='<b> Category </b>'
    )
    return fig

# Ref: https://plotly.com/python/pie-charts/
# callback to display graph for selected category
@app.callback(
    Output('graph-item', 'figure'),
    [Input('dash-monthyear', 'value'),
    Input('dash-category', 'value')]
)
def update_graph_item(month_year, category):
    fig = px.pie(df.query('month_year == @month_year and category ==@category'), 
        values='total', 
        names='name', 
        title= 'Spending for snacks in {}'.format(month_year),
        hole= .5,
    )
    fig.update_traces(
        hoverinfo='label+percent', 
        #text=['$' + total for total in fig.total.values],
        textinfo='value'
    )
    fig.update_layout(
        annotations= [
            dict(text= 'Total Amount <br> $', x=0.5, y=0.5, font_size=15, showarrow=False),
            ],
            legend_title='<b> Item </b>'
    )
    return fig

# Ref: https://plotly.com/python/pie-charts/
# callback to display graph for selected category & month
@app.callback(
    Output('graph-trend', 'figure'),
    [Input('dash-category', 'value')]
)
def update_graph_trend(category):
    fig = px.bar(df.query('category == @category'), x='month_year', y='price', color='category', barmode='group', 
        title= 'Spending History for {}'.format(category),
        labels={
            'category': 'Category', 'price': 'Total Amount', 'month_year': 'Month of Purchase'
        }
    )
    return fig


# Ref: https://plotly.com/python/pie-charts/
# callback to display graph for selected category & month - not updating table on dash page
@app.callback(
    Output('table-spending-category', 'data'),
    [Input('dash-monthyear', 'value'),
    Input('dash-category', 'value')]
)
def update_table(month_year, category):
    df_table = pd.DataFrame(df.query('month_year == @month_year and category == @category'))
    df_table = df_table[['name', 'price', 'quantity', 'total', 'date']]
    print(df_table)
    return df_table.to_dict('records')


# callback for modal
@app.callback(
    Output('modal', 'is_open'),
    [Input('button-new-item', 'n_clicks'), Input('close', 'n_clicks')],
    [State('modal', 'is_open')],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# THIS WORKS except it's adding blank values to df - need exception - look at python exercise #2 for ideas with email exceptions
# Ref: https://dash.plotly.com/advanced-callbacks
# callback to add new item to df + item.csv and update table with new row on submit
@app.callback(
    Output('table-item', 'data'),
    [Input('submit-new-item', 'n_clicks')],
    [State('name', 'value'),
    State('category', 'value'),
    State('price', 'value'),
    State('quantity', 'value'),
    State('date', 'date')
    ]
)
def add_item(n, name, category, price, quantity, date):
    ctx = dash.callback_context
    input_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if input_id == 'submit-new-item':
        df = pd.read_csv("data/items.csv")
        new_row = {'name': name, 'category': category, 'price': price, 'quantity': quantity, 'date': date}
        df = df.append(new_row, ignore_index=True)
        df.to_csv("data/items.csv", index=False)
        print(df)
        return df.to_dict('records')
    else:
        return dash.no_update
        
app.layout = html.Div([navbar, sidebar, dashboard])

if __name__ == '__main__':   
    app.run_server(debug=True)