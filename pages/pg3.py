import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc

dash.register_page(__name__,
                   path='/attribute_exporer',
                   name='Attribute Explorer',
                   title='FP Store Clustering - Attribute Explorer',
                
)

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Class"),
                        dcc.Dropdown(
                            options=[{'label': 'All Classes', 'value': 'class'}, {'label': 'Top Classes', 'value': 'classes'}],
                            value=None,
                            id='filter-choice3',
                            style={'width': '200px'}
                        )
                    ],
                    xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                ),
                dbc.Col(
                    [
                        html.Label("Filter by Class"),
                        dcc.Dropdown(
                            options=[{'label': 'Knit Tops', 'value': 'knits'}, {'label': 'Jeans', 'value': 'jeans'},
                                     {'label': 'Dresses', 'value': 'dress'}, {'label': 'Endless Summer', 'value': 'end'},
                                     {'label': 'Woven Blouses', 'value': 'wove'}],
                            value=None,
                            id='class-choice',
                            style={'width': '200px'}
                        )
                    ],
                    xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Img(id='image-display3', style={'width': '50%'})
                    ],
                    width=12
                )
            ]
        )
    ]
)

@callback(
    Output('image-display3', 'src'),
    Input('filter-choice3', 'value'),
    Input('class-choice', 'value'),
)
def update_image(filter_choice, class_choice):
    if filter_choice == 'class':
        return 'assets/att_all.png'
    elif filter_choice == 'classes':
        if class_choice == 'jeans':
            return 'assets/jeans.png'
        elif class_choice == 'knits':
            return 'assets/knit.png'
        elif class_choice == 'dress':
            return 'assets/dress.png'
        elif class_choice == 'end':
            return 'assets/end.png'
        elif class_choice == 'wove':
            return 'assets/wove.png'
    else:
        return dash.no_update