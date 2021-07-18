# item.py
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import dash_table
from app import app
from dash.dependencies import Input, Output, State
from dash_table import FormatTemplate

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True

df = pd.read_csv("data/items.csv")

CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'padding': '20px 10px'
}

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

# create add item table attributes
app.layout = html.Div(
    [
        html.Br(),
        html.Br(),
        html.H5('Grocery Items'),
        html.Div(
            [
            dbc.Button(
            id='button-new-item',
            n_clicks=0,
            children='New Item',
            color='primary',
            block=True,
            style={'width': '20%', 'textAlign': 'left'}
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
            ],
        ),
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
        #html.Div(id='output-input-form'),
    ],
    style=CONTENT_STYLE
)

# create add item collapse 
def CollapseItem():
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
            ),        
            #dbc.Collapse(
            #    dbc.CardBody(InputItem()),
            #    id='collapse-add-item',
            #    is_open=True,
            #)
        ]
    )
    return collapse_addItem

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


'''
# callback to clear modal inputs
@app.callback(
    Output('name', 'value'),
    Output('category', 'value'),
    Output('price', 'value'),
    Output('quantity', 'value'),
    Output('date', 'date'),
    [Input('submit-new-item', 'n_clicks')]
)
def clear_input(n):
    if n:
        return ''
'''
# HERE: NEED TO GET MODAL TO CLEAR VALUES ON SUBMIT & PUT IN MESSAGES IF VALUES ARE EMPTY


if __name__ == '__main__':
    app.run_server(debug=True)#, dev_tools_hot_reload=False)