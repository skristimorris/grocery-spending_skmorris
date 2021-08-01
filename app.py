# app.py

from __future__ import annotations
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import dash_table
from dash.exceptions import PreventUpdate
from dash import no_update
from dash_table import FormatTemplate

# set dataframe
df = pd.read_csv('data/items.csv')
df_category = pd.read_csv('data/category.csv')
pd.options.display.float_format = '{:.2f}'.format
print(df)

# add 'total' column to df
df['total'] = df['price'] * df['quantity']

# add 'month_year' column to df that assigns month & year to each item based on purchase date
df['month_year'] = pd.to_datetime(df['date']).dt.strftime('%B %Y')
df = df.sort_values(by='date').reset_index(drop=True)

# df for table
df_table = df[['name', 'price', 'quantity', 'date']]

# create variable to select most current month_year date to assign as default value for date dropdown
df_date = df.sort_values(by='date', ascending=False)
df_date = df_date.head(1)
df_date = df_date.month_year.item()

# format price in table as money
money = FormatTemplate.money(2)

# Ref: https://dash.plotly.com/layout
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True

# Ref: https://dash-bootstrap-components.opensource.faculty.ai/docs/components/form/
# create form with inputs to add new item
def InputItem():
    input_addItem = dbc.Form(
        [
            dbc.FormGroup(
                [
                    dbc.Label('Item Name'),
                    dcc.Input(
                        id='name', 
                        placeholder='Enter grocery item',
                        style={'width': '100%'}
                    ),
                ]
            ),
            dbc.FormGroup(
                [
                    html.Label('Category'),
                    dcc.Dropdown(
                        id='category',
                        options=[
                            {'label': i, 'value': i} for i in sorted(df_category.Category)
                        ],
                    )
                ]
            ),
            dbc.FormGroup(
                [
                    html.Label('Price'),
                    dcc.Input(
                        id='price',
                        type='number',
                        placeholder='Enter price of item',
                        style={'width': '100%'}
                    )
                ]
            ),
            dbc.FormGroup(
                [
                    html.Label('Quantity'),
                    dcc.Slider(
                        id='quantity',
                        min=0,
                        max=10,
                        step=1,
                        marks={
                        i: '{}'.format(i)
                        if i == 1
                        else str(i)
                        for i in range(1,11)
                        },
                        value=1,
                    ),
                    html.Br(),
                    html.Label('Date of Purchase'),
                    html.Br(),
                    dcc.DatePickerSingle(
                        id='date',
                        month_format='MMM Do, YY'
                    )
                ]
            ),
                    html.Div(id='output-add-item', 
                    style={'color': 'red'})
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
                dash_table.DataTable(
                        id='table-item',
                        data=df.to_dict('records'),
                        columns=[
                            {
                            'name': i, 'id': i
                            }
                            for i in (df.columns)
                            ],
                        )
            ],
            style={'display': 'none'},
            ),
            html.P('Select a date:'),
            html.Div([
                dcc.Dropdown(
                    id='dash-monthyear',
                    options=[
                        {'label': i, 'value': i} for i in df.month_year.unique()
                    ],
                    value=df_date,
                    clearable=False
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
            html.P('Select a category:'),
            html.Div([
                dcc.Dropdown(id='dash-category',
                clearable=False
                )
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
                dbc.Col([
                        dash_table.DataTable(
                        id='table-item-display',
                        data=df.to_dict('records'),
                        columns=[
                            {'name': 'Name', 'id': 'name'},
                            {'name': 'Price', 'id': 'price', 'type': 'numeric', 'format': FormatTemplate.money(2)},
                            {'name': 'Quantity', 'id': 'quantity'},
                            {'name': 'Date', 'id': 'date'},
                            ],
                        page_action='native',
                        page_current=0,
                        page_size=10,
                        sort_action='native',
                        sort_mode='single',
                        sort_by=[{'column_id': 'date', 'direction': 'desc'}],
                        style_cell={'textAlign': 'left', 'font-family': 'sans-serif'},
                        selected_columns=[],
                        selected_rows=[],
                        style_as_list_view=True,
                        )
                ])
            ]),
            dbc.Row(
                    dcc.Graph(id='graph-trend')
                ),
        ],
        style={
            'margin-left': '15%',
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
        'width': '10%',
        'padding': '20px 10px',
        'background-color': '#f8f9fa'
    }
)

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

# Ref: https://dash-bootstrap-components.opensource.faculty.ai/docs/components/form/
# Check for valid inputs on form
@app.callback(
    Output('output-add-item', 'children'),
    [Input('submit-new-item', 'n_clicks')],
    [State('name', 'value'),
    State('category', 'value'),
    State('price', 'value'),
    State('quantity', 'value'),
    State('date', 'date')]
)
def check_validity(n, name, category, price, quantity, date):
    if n>0:
        if name == None:
            return 'Please enter an item name.'
        if category == None:
            return 'Please select a category.'
        if price == None:
            return 'Please enter a price.'
        if quantity == None:
            return 'Please select a quantity.'
        if date == None:
            return 'Please select a date.'
    else:
        raise PreventUpdate
    

# Ref: https://dash.plotly.com/basic-callbacks
# callback to set category dropdown options based on month selected - not selecting cat for month
@app.callback(
    Output('dash-category', 'options'),
    [Input('dash-monthyear', 'value')]
)
def set_cat_option(month_year):
    df_cat = df.query('month_year == @month_year')
    return [{'label': i, 'value': i} for i in sorted(df_cat.category.unique())]

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
    [Input('table-item', 'data'),
    Input('dash-monthyear', 'value')]
)
def generate_graph_all_cat(data, month_year):
    dff = pd.DataFrame.from_dict(data)
    dff = dff.query('month_year == @month_year')
    dff_total = dff['total'].sum()
    total_format = '{:.2f}'.format(dff_total)

    fig = px.pie(dff, 
        values='total', 
        names='category', 
        title= 'Spending for All Categories in {}'.format(month_year),
        hole= .5)
    fig.update_traces(
        hoverinfo='label+percent', 
        texttemplate='%{value:$}',
        textinfo='value'
    )
    fig.update_layout(
        annotations= [
            dict(text= 'Total Amount <br> ${}'.format(total_format), x=0.5, y=0.5, font_size=15, showarrow=False),
        ],
        legend_title='<b> Category </b>',
        uniformtext_minsize=8,
        uniformtext_mode='show'
    )
    return fig  

# Ref: https://plotly.com/python/pie-charts/
# callback to display graph for selected category
@app.callback(
    Output('graph-item', 'figure'),
    [Input('table-item', 'data'),
    Input('dash-monthyear', 'value'),
    Input('dash-category', 'value')]
)
def update_graph_item(data, month_year, category):
    dff = pd.DataFrame.from_dict(data)
    dff = dff.query('month_year == @month_year and category ==@category')
    dff_total = dff['total'].sum()
    total_format = '{:.2f}'.format(dff_total)

    fig = px.pie(dff, 
        values='total', 
        names='name', 
        title= 'Spending for {} in {}'.format(category, month_year),
        hole= .5,
    )
    fig.update_traces(
        hoverinfo='label+percent', 
        texttemplate='%{value:$}',
        textinfo='value'
    )
    fig.update_layout(
        annotations= [
            dict(text= 'Total Amount <br> ${}'.format(total_format), x=0.5, y=0.5, font_size=15, showarrow=False),
            ],
            legend_title='<b> Item </b>'
    )
    return fig

# Ref: https://plotly.com/python/pie-charts/
# callback to display graph for selected category & month
@app.callback(
    Output('graph-trend', 'figure'),
    [Input('table-item', 'data'),
    Input('dash-category', 'value')]
)
def update_graph_trend(data, category):
    dff = pd.DataFrame.from_dict(data)

    fig = px.bar(dff.query('category == @category'), x='month_year', y='price', color='category', barmode='group', 
        title= 'Spending History for {}'.format(category),
        labels={
            'category': 'Category', 'price': 'Total Amount', 'month_year': 'Month of Purchase'
        }
    )
    fig.update_traces(
        texttemplate='%{value:$}',
        textposition='outside'
    )
    return fig

# Ref: https://dash.plotly.com/advanced-callbacks
# callback to add new item to df + item.csv
@app.callback(
    Output('table-item', 'data'),
    [Input('submit-new-item', 'n_clicks')],
    [State('name', 'value'),
    State('category', 'value'),
    State('price', 'value'),
    State('quantity', 'value'),
    State('date', 'date'),
    ]
)
def update_table(n, name, category, price, quantity, date):
    ctx = dash.callback_context
    input_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if input_id == 'submit-new-item':
        if None not in [name, category, price, quantity, date]:
            df = pd.read_csv("data/items.csv")
            new_row = {'name': name, 'category': category, 'price': price, 'quantity': quantity, 'date': date}
            df = df.append(new_row, ignore_index=True)
            df.to_csv("data/items.csv", index=False)
            df['total'] = df['price'] * df['quantity']
            df['month_year'] = pd.to_datetime(df['date']).dt.strftime('%B %Y')
            df = df.sort_values(by='date').reset_index(drop=True)
            print(df)
            return df.to_dict('records')
        else:
            return no_update
    else:
        return dash.no_update

# callback to update table based on category and date
@app.callback(
    Output('table-item-display', 'data'),
    [Input('dash-monthyear', 'value'),
    Input('dash-category', 'value')]
)
def update_table(month_year, category):
    df_table = pd.DataFrame(df.query('month_year == @month_year and category == @category'))
    df_table = df_table[['name', 'price', 'quantity', 'total', 'date']]
    print(df_table)
    return df_table.to_dict('records')
        
app.layout = html.Div([navbar, sidebar, dashboard])

if __name__ == '__main__':   
    app.run_server(debug=True) 