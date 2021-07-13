# sidebar.py

import dash_html_components as html
from item import CollapseItem
from dashboard import CollapseDashboard

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

# Ref: https://dash-bootstrap-components.opensource.faculty.ai/examples/simple-sidebar/
# create sidebar
layout = html.Div(
    [
    html.Br(),
    html.Br(),
    CollapseDashboard(), # incorporate home button to sidebar
    CollapseItem() # incorporate add item collapse to sidebar
    ],
    style=SIDEBAR_STYLE
)