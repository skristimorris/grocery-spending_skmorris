# app.py

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_html_components.I import I
import plotly.express as px
import pandas as pd
import dash_table
import time

df = pd.read_csv("data/expenses.csv")

# store item name to populate dashboard name dropdown input for selection
#dash_item_name = df.drop_duplicates(subset='name', keep='first', inplace=False).sort_values('name', inplace=False).name.to_string(index=False)
#print(dash_item_name)

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

# Ref: https://dash-bootstrap-components.opensource.faculty.ai/docs/components/navbar/
navbar = dbc.Navbar(
    [
    html.A(
        dbc.Row(
                dbc.Col(dbc.NavbarBrand('Grocery Spending Tracker', className='ml-2')),
            align='left',
            no_gutters=True,
        ),
        ),
    ],
    color='primary',
    dark=True,
    fixed='top'
)
# Ref: https://dash-bootstrap-components.opensource.faculty.ai/docs/components/form/
# create form with inputs to add new item
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
        html.Br(),
        html.Br(),
        html.Div(id='output-date'),
        dbc.Button(
            id='submit_item',
            n_clicks=0,
            children='Submit',
            color='primary',
            block=True,
            style={'width': '40%'}
        ),
        dcc.Loading(
            id='loading-submit-item',
            children=[
                html.Div(
                    [
                        html.Div(
                            id='output-loading-submit-item'
                        )
                    ]
                )
            ],
            type='circle',
        )
    ]
)

# create form with inputs to filter dashboard
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

# Ref: https://dash-bootstrap-components.opensource.faculty.ai/docs/components/collapse/
# create dashboard collapse 
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
            pills=True,
        ),
        dbc.Collapse(
            dbc.CardBody(input_dashboard),
            id='collapse-dashboard',
            is_open=True,
        )
    ]
)

# create add item collapse 
collapse_addItem = html.Div(
    [
        dbc.Nav(
            [
                dbc.NavLink(
                'Add Grocery Item',
                href='/add-item',
                id='button-add-item',
                active='exact',
                n_clicks=0,
                ),
            ],
            pills=True,
        ),        
        dbc.Collapse(
            dbc.CardBody(input_addItem),
            id='collapse-add-item',
            is_open=False,
        )
    ]
)

'''
# create add item collapse 
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
'''

# Ref: https://dash-bootstrap-components.opensource.faculty.ai/examples/simple-sidebar/
# create sidebar attributes
sidebar = html.Div(
    [
    html.Br(),
    html.Br(),
    collapse_dashboard, # incorporate home button to sidebar
    collapse_addItem # incorporate add item collapse to sidebar
    ],
    style=SIDEBAR_STYLE
)

# create content attribute
content = html.Div(
    id='content',
    style=CONTENT_STYLE
)

PAGE_SIZE = 20

# create add item table attributes
table_addItem = html.Div(
    [
        html.Br(),
        html.Br(),
        html.H5('Grocery Items'),
        html.Hr(),
        dash_table.DataTable(
            id='table-add-item',
            columns=[{
                'name': i, 'id': i
            }
            for i in df.columns],
            data=df.to_dict('records'),
            page_current=0,
            page_size=PAGE_SIZE,
            page_action='custom'
        )
    ]
)

# create graphs for dashboard
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

# callback for dashboard collapse
@app.callback(
    Output('collapse-dashboard', 'is_open'),
    [Input('button-dashboard', 'n_clicks')],
    [State('collapse-dashboard', 'is_open')],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

'''
# callback to display graphs when click on dashboard button
@app.callback(
    Output('content','children'),
    [Input('button-add-item', 'n_clicks')]
)
def displayContent(n):
    if n:
        return table_addItem
'''
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

# callback to display content when click on link
@app.callback(
    Output('content', 'children'),
    [Input('url', 'pathname')],
)
def render_content(pathname):
    if pathname == '/dashboard':
        return generate_graphs
    elif pathname == '/add-item':
        return table_addItem

# Ref: https://dash.plotly.com/datatable/callbacks
# callback for table paging
@app.callback(
    Output('table-add-item', 'data'),
    [Input('table-add-item', 'page_current')],
    [Input('table-add-item', 'page_size')]
)
def update_table(page_current, page_size):
    return df.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')

'''
# callback for loading on submit item button
@app.callback(
    Output('output-loading-submit-item', 'children'),
    [Input('loading-submit-item', 'n_clicks')]
)
def input_loading(n):
    time.sleep(1)
    return n
'''
'''
# callback to display graph 1
@app.callback(
    Output('graph_1', 'figure'),
    [Input('button-dashboard', 'n_clicks')],
)
def update_graph_1():
    fig = px.bar(df, x="date", y="price", color="category", barmode="group")
    return fig
'''
'''
# callback to display table when click on add grocery item button
@app.callback(
    Output('content','children'),
    [Input('button-add-item', 'n_clicks'), Input('button-dashboard', 'n_clicks')]
)
def displayContent(n_addItem, n_dashboard):
    if n_dashboard:
        return generate_graphs
    elif n_addItem:
        return table_addItem 
'''

app.layout = html.Div([dcc.Location(id='url'), navbar, sidebar, content])

if __name__ == '__main__':
    app.run_server(debug=True)