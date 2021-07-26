# app.py

from __future__ import annotations
from functools import total_ordering
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import dash_table
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import numpy as np
from datetime import date

df = pd.read_csv('data/items.csv')
df['total'] = df['price'] * df['quantity']
df['month_year'] = pd.to_datetime(df['date']).dt.strftime('%B %Y')

#df['month_year'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
#df['month_year'] = pd.to_datetime(df['date']).dt.to_period('M')
print(df)

#df_group = df.groupby('month_year')['category'].sum().to_frame().reset_index()#
#print(df_group)


#print(df.dtypes)
#df1 = df.groupby(df['date'].dt.strftime('%B %Y'))['total'].sum()
#df_date = df.groupby([(pd.Grouper(key='date', freq='M', sort=True)), 'category'], as_index=False).sum()
#df_date = df.groupby(pd.Grouper(key='date', freq='M', sort=True)).sum()
#df_date.index = df_date.index.strftime('%B %Y')
#print(df_date)
df_group = df.groupby(['month_year', 'category']).sum().sort_values(by=['month_year'], ascending=False)
#df_group_total = df_group[['month_year', 'category', 'total']]
#df_group_total = df_group.drop(df_group.columns[['price', 'quantity']], axis=1, inplace=True)
print(df_group)
#print(df_group_total)

df_cat = pd.read_csv('data/category.csv')

today = date.today()
current_MY = today.strftime('%B %Y')
print(current_MY)

'''
table_1 = pd.pivot_table(df, index=['name'], values=['total'], aggfunc=np.sum)
table_1 = table_1.sort_values(('total'), ascending=False)
#print(table_1)
'''


# Ref: https://dash.plotly.com/layout
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True

# content style attributes
CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'padding': '20px 10px'
}
'''
# sidebar style attributes
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#f8f9fa'
}
'''

# create form with inputs to filter dashboard
def FilterDashboard():
    filter_dashboard = dbc.FormGroup(
        [
            #html.P('Item Name', style={
            #    'textAlign': 'left'
            #}),
            #dcc.Checklist(
            #    id='dash-name-all',
            #    options=[
            #        {'label': 'Select All', 'value': 'all'}
            #    ],
            #    value=[],
            #    #style={'float': 'left'},
            #    labelStyle={'display': 'block'}
            #    #multi=True,
            #),
            #dcc.Dropdown(
            #    id='dash-name',
            #    options=[
            #        {'label': i, 'value': i} for i in sorted(df.name.unique())
            #    ],
            #    multi=True,
            #),
            #html.Br(),
            html.P('Category', style={
                'textAlign': 'left'
            }),
            dcc.Checklist(
                id='dash-category-all',
                options=[
                    {'label': 'Select All', 'value': 'all'}
                ],
                value=[],
                #style={'float': 'left'},
                labelStyle={'display': 'block'}
                #multi=True,
            ),
            dcc.Dropdown(
                id='dash-category',
                options=[
                    {'label': i, 'value': i} for i in sorted(df_cat.Category)
                ],
                value=[1],
                #style={'float': 'left'},
                #labelStyle={'display': 'block'},
                multi=True,
            ),
            html.Br(),
            html.P('Date', style={
                'textAlign': 'left'
            }),
            #dcc.Dropdown(
            #    id='dash-date',
            #    options=[
            #        {'label': i, 'value': i} for i in sorted(df.date.unique())
            #    ],
            #    multi=True,
            #),
            #dcc.Checklist(
            #    id='dash-monthyear-all',
            #    options=[
            #        {'label': 'Select All', 'value': 'all'}
            #    ],
            #    value=[],
            #    #style={'float': 'left'},
            #    labelStyle={'display': 'block'}
            #    #multi=True,
            #),
            dcc.Dropdown(
                id='dash-monthyear',
                options=[
                    {'label': i, 'value': i} for i in sorted(df.month_year.unique())
                ],
                value=current_MY
                #value=[1],
                #style={'float': 'left'},
                #labelStyle={'display': 'block'},
                #multi=True,
            ),
            html.Br(),
            html.Br(),
            #dbc.Button(
                #id='submit-dash',
                #n_clicks=0,
                #children='Filter',
                #color='primary',
                #block=True,
                #style={'width': '40%'}
            #)
        ]
    )
    return filter_dashboard

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


'''
# top 10 items
# Ref: https://pbpython.com/pandas-pivot-table-explained.html
def GenerateGraph_1():
    pv_1 = pd.pivot_table(df.head(), index=['name'], values=['total'], aggfunc=np.sum)
    pv_1 = pv_1.sort_values(('total'), ascending=False)
    trace1 = go.Bar(x=pv_1.index, y=pv_1.values, name='Total')

    graph_1 = dcc.Graph(
            id='graph-1',
            figure={
            'data': [trace1],
            'layout': go.Layout(title='Title', barmode='stack')
                }
        )
    return graph_1
'''
# work on this = graph layout
# Ref: https://dash.plotly.com/dash-core-components/graph
# create graph layout
def GraphLayout():
    graph_layout = html.Div(
        [
            dbc.Row(
                [
                dbc.Col(
                        dcc.Graph(id='graph-3')
                    ),
                #dbc.Col(
                        #dbc.Table(id='graph-4')
                    #)
                ]
                ),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Graph(id='graph-1')
                        ]
                    ),
                    dbc.Col(
                        [
                            dcc.Graph(id='graph-2')
                        ]
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(id='graph-5')
                    ),
                ]
            ),
            dbc.Row(
                dbc.Col(
                        dcc.Graph(id='graph-6')
                ),
            )
        ]
    )
    return graph_layout

# create table for dashboard
def GenerateTable():
    generate_table = html.Div(
        [
            dash_table.DataTable(
            data=df.to_dict('records'),
            id='table-item',
            columns=[
                {
                'name': i, 'id': i
            }
            for i in (df.columns)
            ],
            filter_action='native',
            page_action='native',
            page_current=0,
            page_size=20,
            sort_action='native',
            sort_mode='single',
            sort_by=[{'column_id': 'date', 'direction': 'desc'}],
            style_cell={'textAlign': 'left'},
            selected_columns=[],
            selected_rows=[],
        )
        ]
    )
    return generate_table

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
        button_item,
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
    html.H5('Filter Criteria', style={'textAlign': 'left'}),
    html.Hr(),
    FilterDashboard(),
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

# create dashboard layout
dashboard = html.Div(
    [
    html.Br(),
    html.Br(),
    html.H5('Dashboard', style={'textAlign': 'left'}),
    html.Hr(),
    GraphLayout(),
    html.Br(),
    html.H5('Grocery Items'),
    html.Hr(),
    GenerateTable(),
    ],
    style=CONTENT_STYLE
)
'''
# Ref: https://community.plotly.com/t/check-all-elements-of-dcc-checklist/40854/2
# callback to select all name values
@app.callback(
    Output('dash-name', 'value'),
    [Input('dash-name-all', 'value')],
    [State('dash-name', 'options')]
)
def select_all(all_selected, options):
    selected = []
    selected = [option['value'] for option in options if all_selected]
    return selected
'''

# Ref: https://community.plotly.com/t/check-all-elements-of-dcc-checklist/40854/2
# callback to select all category values
@app.callback(
    Output('dash-category', 'value'),
    [Input('dash-category-all', 'value')],
    [State('dash-category', 'options')]
)
def select_all(all_selected, options):
    selected = []
    selected = [option['value'] for option in options if all_selected]
    return selected

# callback to display graph 1
@app.callback(
    Output('graph-1', 'figure'),
    [Input('dash-category', 'value'),
    Input('dash-monthyear', 'value')]
)
def update_graph_1(category, month_year):
    fig = px.bar(df.query('category == @category and month_year == @month_year'), x='month_year', y='price', color='category', barmode='group', 
        title= 'Spending per Category by Month',
        labels={
            'category': 'Category', 'price': 'Total Amount', 'month_year': 'Month of Purchase'
        }
    )
    print(month_year)
    return fig

# Ref: https://plotly.com/python/pie-charts/
# callback to display graph 3 - work on this monthyear not pulling graph info
@app.callback(
    Output('graph-3', 'figure'),
    [Input('dash-monthyear', 'value')]
)
def update_graph_3(month_year):
    #query_graph3 = df.query('month_year == @month_year').sum()
   
    fig = px.pie(df.query('month_year == @month_year'), 
        values='total', 
        names='category', 
        title= 'Spending per Category for {}'.format(month_year),
        hole= .5,
        #labels={
            #'category': 'Category', 'total': 'Total Amount'
        #}
    )
    fig.update_traces(
        hoverinfo='label+percent', 
        #text=['$' + total for total in fig.total.values],
        textinfo='value'
    )
    fig.update_layout(
        annotations= [
            dict(text= 'Total Amount <br> $', x=0.5, y=0.7, font_size=15, showarrow=False),
            #dict(text= '$', x=0.5, y=0.5, font_size=15, showarrow=False),
            #dict(text= 'Total Amount: $', x=0.5, y=0.5, font_size=15, showarrow=False)
            ],
            legend_title='<b> Category </b>'
    )
    #print(query_graph3)
    return fig
'''
# Ref: https://plotly.com/python/pie-charts/
# callback to display graph 4 - work on this monthyear not pulling graph info
@app.callback(
    Output('graph-4', 'children'),
    [Input('dash-monthyear', 'value')]
)
def update_graph_4(month_year):
    query_graph4 = df.query('month_year == @month_year')
    df_group = pd.DataFrame(query_graph4.groupby(['month_year', 'category']).sum().sort_values(by=['month_year'], ascending=False))
    df_group = df_group[['category, total']]
    print(df_group)
    #print(query_graph4)
    return dbc.Table.from_dataframe(
        df_group, striped=True, bordered=True, hover=True
    )
'''
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