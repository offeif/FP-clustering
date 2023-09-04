import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

dash.register_page(__name__,
                   path='/image_explorer',  # represents the url text
                   name='Image Explorer',  # name of page, commonly used as name of link
                   title='FP Store Clustering - Image Explorer'  # epresents the title of browser's tab
)

# page 2 data
df = pd.read_csv('test_df_net.csv')

# Define your clusters and their corresponding image filenames
clusters = ['Cluster 1', 'Cluster 2', 'Cluster 3', 'Cluster 4', 'Cluster 5', 'Cluster 6']
top_5 = ['Knit Tops', 'Jeans', 'Dresses', 'Endless Summer', 'Woven Blouses']
options = ['Clusters', 'Top Classes']

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [html.Label("Select Option"),
                     dcc.Dropdown(options=[{'label': opt, 'value': opt} for opt in options],
                                  id='option-choice', style={'width': '200px'})
                     ], xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                ),
                dbc.Col(
                    [html.Label("Select a Cluster"),
                     dcc.Dropdown(id='cluster-choice', style={'width': '200px'}, disabled=True)
                     ], xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                ),
                dbc.Col(
                    [html.Label("Filter By"),
                     dcc.Dropdown(id='filter-choice', style={'width': '200px'}, disabled=True)
                     ], xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [html.Img(id='image-display', style={'width': 'auto'})], width=12
                )
            ]
        )
    ]
)



@callback(
    Output('cluster-choice', 'options'),
    Output('filter-choice', 'options'),
    Input('option-choice', 'value')
)
def update_options(selected_option):
    if selected_option == 'Clusters':
        cluster_options = [{'label': f'Cluster {i + 1}', 'value': cluster} for i, cluster in enumerate(clusters)]
        filter_options = []
    elif selected_option == 'Top Classes':
        cluster_options = [{'label': f'Cluster {i + 1}', 'value': cluster} for i, cluster in enumerate(clusters)]
        filter_options = [{'label': top, 'value': top} for top in top_5]
    else:
        cluster_options = []
        filter_options = []

    return cluster_options, filter_options


@callback(
    Output('cluster-choice', 'disabled'),
    Output('filter-choice', 'disabled'),
    Input('option-choice', 'value')
)
def disable_dropdowns(selected_option):
    if selected_option is None:
        return True, True  # Disable both dropdowns if no option is selected
    else:
        return False, False  # Enable both dropdowns if an option is selected


@callback(
    Output('image-display', 'src'),
    Input('cluster-choice', 'value'),
    Input('filter-choice', 'value'),
)
def update_image(cluster, filter_choice):
    if cluster is None:
        return dash.no_update

    if filter_choice is None:
        image_filename = f'assets/{cluster}.png'
    else:
        # Assuming you have a folder structure like 'assets/Cluster 1/Knit Tops.png'
        image_filename = f'assets/top/{filter_choice}/{cluster}.png'

    return image_filename
