import dash
from dash import dcc, html, callback, Output, Input, dash_table
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import State

dash.register_page(__name__,
                   path='/data_explorer',  # represents the url text
                   name='Data Explorer',  # name of page, commonly used as name of link
                   title='FP Store Clustering - Data Explorer'  # represents the title of browser's tab
)

# page 2 data
df = pd.read_csv('test_df_net.csv')

# cluster_1 = pd.read_csv('datasets/cluster_1.csv')
# cluster_2 = pd.read_csv('datasets/cluster_2.csv')
# cluster_3 = pd.read_csv('datasets/cluster_3.csv')
# cluster_4 = pd.read_csv('datasets/cluster_4.csv')
# cluster_5 = pd.read_csv('datasets/cluster_5.csv')

# cluster_1_store = pd.read_csv('datasets/cluster_1_store.csv')
# cluster_1_class = pd.read_csv('datasets/cluster_1_class.csv')
# cluster_1_att = pd.read_csv('datasets/cluster_1_att.csv')

# cluster_2_store = pd.read_csv('datasets/cluster_2_store.csv')
# cluster_2_class = pd.read_csv('datasets/cluster_2_class.csv')
# cluster_2_att = pd.read_csv('datasets/cluster_2_att.csv')

# cluster_3_store = pd.read_csv('datasets/cluster_3_store.csv')
# cluster_3_class = pd.read_csv('datasets/cluster_3_class.csv')
# cluster_3_att = pd.read_csv('datasets/cluster_3_att.csv')

# cluster_4_store = pd.read_csv('datasets/cluster_4_store.csv')
# cluster_4_class = pd.read_csv('datasets/cluster_4_class.csv')
# cluster_4_att = pd.read_csv('datasets/cluster_4_att.csv')

# cluster_5_store = pd.read_csv('datasets/cluster_5_store.csv')
# cluster_5_class = pd.read_csv('datasets/cluster_5_class.csv')
# cluster_5_att = pd.read_csv('datasets/cluster_5_att.csv')

# Define your clusters and their corresponding image filenames
filter_by = ['Store Info', 'Class', 'Attribute']


layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Select a Cluster"),
                        dcc.Dropdown(
                            options=[
                                {'label': cluster, 'value': cluster}
                                for cluster in sorted(df['cluster'].unique())
                            ],
                            id='cluster-choice2',
                
                            style={'width': '200px'}
                        )
                    ],
                    xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                ),
                dbc.Col(
                    [
                        html.Label("Filter By"),
                        dcc.Dropdown(
                            options=[{'label': top, 'value': top} for top in filter_by],
                            id='filter-choice2',
                            style={'width': '200px'}
                        )
                    ],
                    xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                ),
            ]
        ),
        html.Div(style={'margin-top': '50px'}),  # Add spacing between dropdowns and table
        dbc.Row(
            [
                dbc.Col(
                    [
                        dash_table.DataTable(
                            id='dataframe-display2',
                            columns=[],
                            page_size=15,  # Set the default number of rows per page
                            page_action='native',  # Enable built-in pagination
                            page_current=0,  # Set the initial page to 0
                           filter_action="native",
                            sort_action="native",
                            sort_mode='multi',
                        
                            style_cell={
                                'fontSize': 14,
                                'font-family': 'Roboto',
                                'height': 'auto',
                                'minWidth': '320px',
                                'width': '320px',
                                'maxWidth': '320px',
                                'whiteSpace': 'normal',
                                'textAlign': 'center',
                                'padding': '10px',
                                'borderLeft': 'none',  # Remove left cell border
                                'borderRight': 'none',  # Remove right cell border
                            },
                            style_header={
                                'border': 'none',
                                'fontWeight': 'bold',
                                'borderBottom': '1px solid #333'
                            },
                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'even'},
                                    'backgroundColor': 'rgb(249, 249, 249)',
                                }
                            ]
                        )
                    ],
                    width=12
                )
            ]
        )
    ]
)

@callback(
    Output('dataframe-display2', 'data'),
    Output('dataframe-display2', 'columns'),
    Input('cluster-choice2', 'value'),
    Input('filter-choice2', 'value'),
)
def update_dataframe(cluster, filter_choice):
    if cluster is None:
        return dash.no_update, []

    base_path = 'datasets/'  # Using absolute path  # Change this path according to your folder structure

    if filter_choice == 'Store Info':
        dataframe_path = f'{base_path}{cluster}_store.csv'
    elif filter_choice == 'Class':
        dataframe_path = f'{base_path}{cluster}_class.csv'
    elif filter_choice == 'Attribute':
        dataframe_path = f'{base_path}{cluster}_att.csv'
    else:
        dataframe_path = f'{base_path}{cluster}.csv'  # Default to the basic cluster dataframe

    dataframe = pd.read_csv(dataframe_path)

    # Add row numbers as a new column at the beginning of the DataFrame
    dataframe.insert(0, 'Row Number', range(1, len(dataframe) + 1))

    columns = [{'name': col, 'id': col} for col in dataframe.columns]

    # Remove the 'Row Number' column name
    columns[0]['name'] = ''

    return dataframe.to_dict('records'), columns
