"""Track and analyze grocery spending at an item level.

This app allows a user to input a grocery item.

"""

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
from datetime import date

df = pd.read_csv('data/items.csv') # read items.csv file into df
df_category = pd.read_csv('data/category.csv') # read category.csv file into df
pd.options.display.float_format = '{:.2f}'.format # set pandas format to 2 decimals

df['total'] = df['price'] * df['quantity'] # add 'total' column to df

df['month_year'] = pd.to_datetime(df['date']).dt.strftime('%B %Y') # add 'month_year' column to df and convert to 'month year' str format
df = df.sort_values(by='date').reset_index(drop=True) # sort df by date and reset and drop index

df_table = df[['name', 'price', 'quantity', 'date']] # create df to display table in layout

df_date = df.sort_values(by='date', ascending=False) # sort df by date in descending order and set to variable
df_date = df_date.head(1) # select top row of df
df_date = df_date.month_year.item() # select value from 'month_year' column to use as default in date dropdown

# Ref: https://dash.plotly.com/layout
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True

# Ref: https://dash-bootstrap-components.opensource.faculty.ai/docs/components/form/
def InputItem():
    """Create a form with inputs to add a new item.
    
    Args:
        none
    
    Returns:
        item name: input text field to enter item name
        category: dropdown to select category
        price: input numeric field to enter price
        quantity: slider to select quantity
        date: date picker to select date of purchase
        output: text to show exceptions
    """
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
                        month_format='MMM Do, YY',
                        date=date.today()
                    )
                ]
            ),
                    html.Div(id='output-add-item',
                    style={'color': 'red'})
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
            dbc.Button('Cancel', id='cancel', className='ml-auto', n_clicks=0, color='primary')
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

# Ref: https://dash.plotly.com/dash-core-components/graph
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
sidebar = html.Div(
    [
    html.Br(),
    html.Br(),
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

@app.callback(
    Output('modal', 'is_open'),
    Output('output-add-item', 'children'),
    [Input('button-new-item', 'n_clicks'), 
    Input('cancel', 'n_clicks'),
    Input('submit-new-item', 'n_clicks')],
    [State('modal', 'is_open'),
    State('name', 'value'),
    State('category', 'value'),
    State('price', 'value')
    ]
)
def toggle_modal(n1, n2, n3, is_open, name, category, price):
    """Callback to toggle modal.
    
    Args:
        n1: number of times new item button is clicked
        n2: number of times cancel button is clicked
        n3: number of times submit button is clicked
        is_open: passes open state of modal
        name: passes state of item name value
        category: passes state of category value
        price: passes state of price value
    
    Returns:
        enables modal to be toggled between open and closed when the buttons are clicked,
        if submit button is clicked and name, category or price is empty (quantity & date have default values):
            modal does not close and string displays with missing input fields 
    """
    ctx = dash.callback_context
    input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if input_id == 'button-new-item':
        return not is_open, None
    elif input_id == 'cancel':
        return not is_open, None
    elif input_id == 'submit-new-item':
        if name == None:
            return dash.no_update, 'Please enter an item name.'
        if category == None:
            return dash.no_update, 'Please select a category.'
        if price == None:
            return dash.no_update, 'Please enter a price.'
        return not is_open, None
    return is_open, None

@app.callback(
    [Output('name', 'value'),
    Output('category', 'value'),
    Output('price', 'value'),
    Output('quantity', 'value'),
    Output('date', 'date')],
    [Input('modal', 'is_open')]
)
def clear_input(is_open):
    """Callback to clear input values when modal is opened.
        
        Args:
            is_open: open state of modal
        
        Returns:
            None for name, category, and price inputs and resets quantity slider to 1 and date to today's date
    """
    return (None,None,None,1,date.today())

# Ref: https://dash.plotly.com/basic-callbacks
@app.callback(
    Output('dash-category', 'options'),
    [Input('table-item', 'data'),
    Input('dash-monthyear', 'value')]
)
def set_cat_option(data, month_year):
    """Callback to set category dropdown options based on the month selected.
        
        Args:
            data: dataframe
            month_year: selected date from dropdown
        
        Returns:
            list of categories into category dropdown from dataframe for selected date
    """
    dff = pd.DataFrame.from_dict(data)
    dff = dff.query('month_year == @month_year')
    return [{'label': i, 'value': i} for i in sorted(dff.category.unique())]

@app.callback(
    Output('dash-category', 'value'),
    [Input('dash-category', 'options')]
)
def set_cat_default(available_options):
    """Callback to set category dropdown default value.
        
        Args:
            available_options: list of categories from dropdown
        
        Returns:
            first value from category dropdown to set as default dropdown value
    """
    return available_options[0]['value']


# Ref: https://plotly.com/python/pie-charts/
@app.callback(
    Output('graph-spending-all', 'figure'),
    [Input('table-item', 'data'),
    Input('dash-monthyear', 'value')]
)
def generate_graph_all_cat(data, month_year):
    """Callback to generate graph to show spending in all categories for the selected month.
        
        Args:
            data: dataframe
            month_year: selected date from dropdown
        
        Returns:
            pie chart dispalying amounts spent per category and total amount spent for selected month
    """
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
        texttemplate='%{value:$.2f}',
        textposition='inside'
    )
    fig.update_layout(
        annotations= [
            dict(text= 'Total Amount <br> ${}'.format(total_format), x=0.5, y=0.5, font_size=15, showarrow=False),
        ],
        legend_title='<b> Category </b>'
    )
    return fig  

# Ref: https://plotly.com/python/pie-charts/
@app.callback(
    Output('graph-item', 'figure'),
    [Input('table-item', 'data'),
    Input('dash-monthyear', 'value'),
    Input('dash-category', 'value')]
)
def update_graph_item(data, month_year, category):
    """Callback to generate graph to show amounts spent per item for the selected month and category.
        
        Args:
            data: dataframe
            month_year: selected date from dropdown
            category: selected category from dropdown
        
        Returns:
            pie chart dispalying amounts spent per item and total amount spent for selected month and category 
    """
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
@app.callback(
    Output('graph-trend', 'figure'),
    [Input('table-item', 'data'),
    Input('dash-category', 'value')]
)
def update_graph_trend(data, category):
    """Callback to generate graph to show amounts spent in all months for the selected category.
        
        Args:
            data: dataframe
            category: selected category from dropdown
        
        Returns:
            bar chart dispalying amounts spent per month for selected category 
    """
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
    """Callback to add new item to dataframe and write to csv file.
        
        Args:
            n: number of times submit button is clicked
            name: passes state of item name value
            category: passes state of category value
            price: passes state of price value
            quantity: passes state of quantity value
            date: passes state of date value
        
        Returns:
            dataframe with appended new row to hidden datatable in dashboard layout

        Raises:
            no update to dataframe if name, category, price, quantity, or date is empty 
    """
    df = pd.read_csv("data/items.csv")
    ctx = dash.callback_context
    input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if input_id == 'submit-new-item':
        if None in [name, category, price]:
            return dash.no_update
        else:
            new_row = {'name': name, 'category': category, 'price': price, 'quantity': quantity, 'date': date}
            df = df.append(new_row, ignore_index=True)
            df.to_csv("data/items.csv", index=False)
            df['total'] = df['price'] * df['quantity']
            df['month_year'] = pd.to_datetime(df['date']).dt.strftime('%B %Y')
            df = df.sort_values(by='date').reset_index(drop=True)
            return df.to_dict('records')
    else:
        df['total'] = df['price'] * df['quantity']
        df['month_year'] = pd.to_datetime(df['date']).dt.strftime('%B %Y')
        df = df.sort_values(by='date').reset_index(drop=True)
        return df.to_dict('records')

@app.callback(
    Output('table-item-display', 'data'),
    [Input('table-item', 'data'),
    Input('dash-monthyear', 'value'),
    Input('dash-category', 'value')]
)
def update_table_display(data, month_year, category):
    """Callback to update datatable based on date and category dropdown selection.
        
        Args:
            data: dataframe
            month_year: selected date from dropdown
            category: selected category from dropdown
        
        Returns:
            datatable dispalying items for selected month and category 
    """
    dff = pd.DataFrame.from_dict(data)
    df_table = pd.DataFrame(dff.query('month_year == @month_year and category == @category'))
    return df_table.to_dict('records')
        
app.layout = html.Div([navbar, sidebar, dashboard])

if __name__ == '__main__':
    app.run_server(debug=True)