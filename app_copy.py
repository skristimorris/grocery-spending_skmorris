# app.py

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import dash_table
from dash_table import FormatTemplate
from dash.exceptions import PreventUpdate

df = pd.read_csv("data/items.csv")

# Ref: https://dash.plotly.com/layout
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True
'''
# create content for layout
content = html.Div(
    id='content',
)
'''
# content style attributes
CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'padding': '20px 10px'
}

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
'''
# Ref: https://dash-bootstrap-components.opensource.faculty.ai/docs/components/collapse/
# create dashboard collapse 
def CollapseDashboard():
    collapse_dashboard = html.Div(
        #[
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
            #dbc.Collapse(
                #dbc.CardBody(InputDashboard()),
                #id='collapse-dashboard',
                #is_open=True,
            #)
        #]
    )
    return collapse_dashboard
'''

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
                "New Item", id='button-new-item', color="primary", className="ml-2", n_clicks=0
            ),
            #width="auto",
        ),
        dbc.Modal(
        [
        dbc.ModalHeader('Add New Item'),
        dbc.ModalBody(InputItem()),
        dbc.ModalFooter(
            [
            dbc.Button('Submit', id='submit-new-item', className='ml-auto', n_clicks=0),
            dbc.Button('Close', id='close', className='ml-auto', n_clicks=0)
            ]
        )
        ],
        id='modal',
        is_open=False,
    )
    ],
    no_gutters=True,
    className="ml-auto flex-nowrap mt-3 mt-md-0",
    align="center",
),
])

# create graphs for dashboard
def GenerateGraphs():
    generate_graphs = html.Div(
        [
            html.Br(),
            html.Br(),
            #html.H5('Dashboard'),
            #html.Hr(),
            dbc.Col(dcc.Graph(
                id='graph_1',
                figure = px.bar(df, x="date", y="price", color="category", barmode="group"),
            )
            )
        ]
    )
    return generate_graphs
'''
# create dashboard layout
layout = html.Div(
    [
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.H5('Dashboard', style={
                'textAlign': 'left'
            }),
    ]),
        dbc.Col([
            dbc.Button(
                id='button-new-item',
                n_clicks=0,
                children='New Item',
                color='primary',
                block=True,
                style={'width': '20%', 'textAlign': 'center', 'verticalAlign': 'right'}
                ),
                dbc.Modal(
                    [
                    dbc.ModalHeader('Add New Item'),
                    dbc.ModalBody(InputItem()),
                    dbc.ModalFooter(
                        [
                        dbc.Button('Submit', id='submit-new-item', className='ml-auto', n_clicks=0),
                        dbc.Button('Close', id='close', className='ml-auto', n_clicks=0)
                        ]
                    )
                    ],
                    id='modal',
                    is_open=False,
                ),
        ]),
    html.Hr(),
        ],
    ),
    GenerateGraphs()
    ],
    style=CONTENT_STYLE
)
'''





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
    color="primary",
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
    InputDashboard(),
    #CollapseItem() 
    ],
    style=SIDEBAR_STYLE
)

# create dashboard layout
dashboard = html.Div(
    [
    html.Br(),
    html.Br(),
    html.H5('Dashboard', style={'textAlign': 'left'}),
    html.Hr(),
    GenerateGraphs(),
    html.Br(),
        html.H5('Grocery Items'),
        html.Hr(),
        html.Div(id='output-layout'),
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
        ),
    ],
    style=CONTENT_STYLE
)

'''
# callback to display content when click on link
@app.callback(
    Output('content', 'children'),
    [Input('url', 'pathname')],
)
def render_content(pathname):
    if pathname == '/dashboard':
        return dashboard.layout
    elif pathname == '/add-item':
        return item.layout
'''
'''
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

# callback for modal - work on this in the AM
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


#app.layout = html.Div([dcc.Location(id='url'), navbar.Navbar(), sidebar.layout, dashboard.layout])
app.layout = html.Div([navbar, sidebar, dashboard])

if __name__ == '__main__':   
    app.run_server(debug=True)