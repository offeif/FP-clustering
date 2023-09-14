import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SANDSTONE])
server = app.server

sidebar = dbc.Nav(
    [
        dbc.NavLink(
            [
                html.Div(page["name"], className="ms-2"),
            ],
            href=page["path"],
            active="exact",
        )
        for page in dash.page_registry.values()
    ],
    pills=True,
    className="bg-light d-flex justify-content-center",  # Center the nav bar horizontally
)

app.layout = dbc.Container([
    html.Div(
        [
            sidebar,
            dbc.Row(
                dbc.Col(
                    [
                        html.Div("FP Store Clustering", style={'fontSize': 40, 'textAlign': 'center', 'color': '#808080'}),
                        html.Div("Using Net Amount 2022-01-01 and 2022-12-31", style={'fontSize': 15, 'textAlign': 'center', 'color': '#808080', 'fontStyle': 'italic'}),
                    ],
                    width={"size": 10, "offset": 1},  # Center the heading horizontally
                ),
            ),
        ],
        className="mb-4",  # Add margin at the bottom for spacing
    ),

    html.Hr(),

    dbc.Row(
        [
            dbc.Col(
                [
                    dash.page_container
                ], xs=12, sm=12, md=12, lg=12, xl=12, xxl=12
            )
        ]
    )
], fluid=True)

if __name__ == "__main__":
    app.run(debug=False)
