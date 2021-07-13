# navbar.py

import dash_html_components as html
import dash_bootstrap_components as dbc

# Ref: https://dash-bootstrap-components.opensource.faculty.ai/docs/components/navbar/
def Navbar():
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
    return navbar