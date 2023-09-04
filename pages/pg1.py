import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

px.set_mapbox_access_token(open("map.txt").read())

# To create meta tag for each page, define the title, image, and description.
dash.register_page(__name__,
                   path='/',  # '/' is home page and it represents the url
                   name='Interactive Map',  # name of page, commonly used as name of link
                   title='FP Store Clustering - Interactive Map',  # title that appears on browser's tab
                   
)

# page 1 data
# Create a sample DataFrame with your data
# Sample DataFrame
# data = {
#     'store name': ['Store A', 'Store B', 'Store C'],
#     'latitude': [40.62718, 40.63718, 40.74718],
#     'longitude': [-73.29494, -73.30494, -73.31494],
#     'cluster': ['Cluster 1', 'Cluster 2', 'Cluster 3']
# }

# df = pd.DataFrame(data)
df = pd.read_csv('test_df_net.csv')

# Your layout code remains the same
# Create an information div that will display the cluster information
info_div = html.Div(id='cluster-info', style={'padding': '20px', 'color': '#808080'})

# Modify the layout to include the info_div
layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [html.Label("Select a Cluster"),
                     dcc.Dropdown(
                         options=[
                             {'label': 'All', 'value': 'All'}
                         ] + [{'label': cluster, 'value': cluster} for cluster in sorted(df['cluster'].unique())],
                         id='cluster-choice',
                         value='All',
                         style={'width': '200px'}
                     ),
                     ],
                    xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='map-fig', style={'height': '100vh', 'border': '0'})
                    ],
                    style={'position': 'relative', 'height': '100vh', 'width': '100vh'}
                ),
                dbc.Col(
                    [
                        info_div  # Display the cluster information div
                    ],
                    xs=10, sm=10, md=4, lg=4, xl=4, xxl=4,
                    style={'border': '1px solid #ccc', 'height': '60%', 'width': '15%', 'overflow-y': 'auto'}
                )
            ]
        )
    ]
)

@callback(
    [Output('map-fig', 'figure'),
     Output('cluster-info', 'children')],  # Also update the cluster information div
    Input('cluster-choice', 'value')
)
def update_map_and_info(selected_cluster):
    if selected_cluster == 'All':
        dff = df
    else:
        dff = df[df['cluster'] == selected_cluster]

    # Calculate the store count per cluster
    cluster_store_counts = dff['cluster'].value_counts()

    # Calculate marker sizes based on store counts
    marker_sizes = [cluster_store_counts.get(cluster, 0) for cluster in dff['cluster']]

    # Create a mapbox figure using Plotly Graph Objects scattermapbox
    color_mapping = {'Cluster 1': '#3FE0D0', 'Cluster 2': '#95C8D8', 'Cluster 3': '#588BAE', 
                     'Cluster 4': '#4682B4', 'Cluster 5': '#7285A5', 'Cluster 6': '#06214F'}

    fig = go.Figure()

    for i, (cluster_name, color) in enumerate(color_mapping.items()):
        cluster_data = dff[dff['cluster'] == cluster_name]
        fig.add_trace(go.Scattermapbox(
            lat=cluster_data['latitude'],
            lon=cluster_data['longitude'],
            mode='markers',
            marker=dict(
                size=17,
                color=color
            ),
            customdata=cluster_data[['store_num', 'store_name', 'grade', 'store_format', 'total_net_amt_ly']],
            hovertemplate=(
                "<b>Store Num</b>: %{customdata[0]}<br><br>" +
                "Store Name: %{customdata[1]}<br>" +
                "Grade: %{customdata[2]}<br>" +
                "Store Format: %{customdata[3]}<br>" +
                "Total Net Amt LY: %{customdata[4]:$,.0f}<br>"
                "<extra></extra>"
            ),
            name=cluster_name,  # Set the legend title
            legendgroup=f"cluster-{i}"  # Set the legend group
        ))

    fig.update_layout(
        mapbox_style='carto-positron',
        mapbox_center={'lat': 37.0902, 'lon': -95.7129},
        mapbox_zoom=4,
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
        ),
        showlegend=True  # Show the legend
    )

    # Example: Cluster information for different clusters
    cluster_info_dict = {
        'Cluster 1': html.Div([
        html.Strong("Cluster Size:"),
        html.Br(),
        "43",
        html.Br(),
        html.Strong("Grade:"),
        html.Br(),
        "F + UNKNOWN",
        html.Br(),
        html.Strong("Climate:"),
        html.Br(),
        "Hot, Cold",
        html.Br(),
        html.Strong("Region:"),
        html.Br(),
        "EAST COAST-NEW ENGLAND and EAST COAST-NORTHEAST",
        html.Br(),
        html.Br(),
        html.Strong("This cluster over-indexed the most in:"),
        html.Br(),
        "Divisions: Apparel Division, Intimate Apparel, Beauty",
        html.Br(),
        "Classes: Movement Hats, Heavy Knits, Sweaters, Movement Heavyweights, Casual Outerwear",
        html.Br(),
        html.Br(),
        html.Strong("This Cluster under-indexed the most in:"),
        html.Br(),
        "Classes: Sunglasses, Swim Bottoms, Jeans, Performance Outerwear, Shorts",
    ], style={'font-family': 'Arial, sans-serif', 'font-size': '16px'}),
    'Cluster 2': html.Div([
        html.Strong("Cluster Size:"),
        html.Br(),
        "34",
        html.Br(),
        html.Strong("Grade:"),
        html.Br(),
        "F + UNKNOWN",
        html.Br(),
        html.Strong("Climate:"),
        html.Br(),
        "Mild, Cold",
        html.Br(),
        html.Strong("Region:"),
        html.Br(),
        "CENTRAL-MID-WEST DISTRICT and WEST COAST-NORTHWEST",
        html.Br(),
        html.Br(),
        html.Strong("This cluster over-indexed the most in:"),
        html.Br(),
        "Divisions: Movement",
        html.Br(),
        "Classes: Casual One Piece, Heavy Knits, Movement Heavyweights, Casual Layering, Performance Camis",
        html.Br(),
        html.Br(),
        html.Strong("This Cluster under-indexed the most in:"),
        html.Br(),
        "Classes: Performance Bottoms, Jewelry, Woven Blouses, Shorts, Hats",
    ], style={'font-family': 'Arial, sans-serif', 'font-size': '16px'}),
    'Cluster 3': html.Div([
        html.Strong("Cluster Size:"),
        html.Br(),
        "33",
        html.Br(),
        html.Strong("Grade:"),
        html.Br(),
        "F + UNKNOWN",
        html.Br(),
        html.Strong("Climate:"),
        html.Br(),
        "Mild, Hot",
        html.Br(),
        html.Strong("Region:"),
        html.Br(),
        "CENTRAL-TEXAS and EAST COAST-SOUTHEAST DISTRICT",
        html.Br(),
        html.Br(),
        html.Strong("This cluster over-indexed the most in:"),
        html.Br(),
        "Divisions: Vintage, Movement",
        html.Br(),
        "Classes: Performance Shorts, Performance Layering, Casual Shorts, Casual Sets, Performance Camis",
        html.Br(),
        html.Br(),
        html.Strong("This Cluster under-indexed the most in:"),
        html.Br(),
        "Classes: Boots, Beach, Woven Blouses, Sunsuits, Lounge",
    ], style={'font-family': 'Arial, sans-serif', 'font-size': '16px'}),
    'Cluster 4': html.Div([
        html.Strong("Cluster Size:"),
        html.Br(),
        "30",
        html.Br(),
        html.Strong("Grade:"),
        html.Br(),
        "F + UNKNOWN",
        html.Br(),
        html.Strong("Climate:"),
        html.Br(),
        "Hot, Mild",
        html.Br(),
        html.Strong("Region:"),
        html.Br(),
        "WEST COAST-SOUTHERN CALIFORNIA and CENTRAL-MOUNTAIN",
        html.Br(),
        html.Br(),
        html.Strong("This cluster over-indexed the most in:"),
        html.Br(),
        "Divisions: Vintage, Apparel Division, Intimate Apparel",
        html.Br(),
        "Classes: Casual One Piece, Shorts, Performance Camis, Knit Tops, Surf One Piece",
        html.Br(),
        html.Br(),
        html.Strong("This Cluster under-indexed the most in:"),
        html.Br(),
        "Classes: Bras Movement, Surf Tops, Casual Shorts, Sandals, Performance Bottom",
    ], style={'font-family': 'Arial, sans-serif', 'font-size': '16px'}),
    'Cluster 5': html.Div([
        html.Strong("Cluster Size:"),
        html.Br(),
        "29",
        html.Br(),
        html.Strong("Grade:"),
        html.Br(),
        "F + UNKNOWN",
        html.Br(),
        html.Strong("Climate:"),
        html.Br(),
        "Mild, Cold",
        html.Br(),
        html.Strong("Region:"),
        html.Br(),
        "WEST COAST-LOS ANGELES and WEST COAST-MVMT - WEST COAST",
        html.Br(),
        html.Br(),
        html.Strong("This cluster over-indexed the most in:"),
        html.Br(),
        "Divisions: Intimate Apparel, Womens Accessories, Apparel Division",
        html.Br(),
        "Classes: Suits, Underwire Bras, In case Jewelry, Surf Bottoms, Outerwear, Undies",
        html.Br(),
        html.Br(),
        html.Strong("This Cluster under-indexed the most in:"),
        html.Br(),
        "Classes: Casual Bottoms, Performance, Bottoms, Sweaters, Knit Tops",
    ], style={'font-family': 'Arial, sans-serif', 'font-size': '16px'}),
    'Cluster 6': html.Div([
        html.Strong("Cluster Size:"),
        html.Br(),
        "13",
        html.Br(),
        html.Strong("Grade:"),
        html.Br(),
        "A1 + UNKNOWN",
        html.Br(),
        html.Strong("Climate:"),
        html.Br(),
        "Hot, Cold",
        html.Br(),
        html.Strong("Region:"),
        html.Br(),
        "EAST COAST-FLORIDA and EAST COAST-MVMT - EAST COAST",
        html.Br(),
        html.Br(),
        html.Strong("This cluster over-indexed the most in:"),
        html.Br(),
        "Divisions: Movement, Apparel Division, Intimate Apparel",
        html.Br(),
        "Classes: Surf One Piece, Performance One Pieces, Party dresses, Performance Bottoms, Bras Movement",
        html.Br(),
        html.Br(),
        html.Strong("This Cluster under-indexed the most in:"),
        html.Br(),
        "Classes: Casual Layering, Knit Tops, Performance Shorts, Movement Bags, Trend Shoes",
    ], style={'font-family': 'Arial, sans-serif', 'font-size': '16px'}),
    # Similarly format other clusters...
}

   # Create cluster information HTML
    if selected_cluster == 'All':
        cluster_info_html = None  # No cluster information for 'All'
    else:
        cluster_info_html = cluster_info_dict[selected_cluster]

    return fig, cluster_info_html