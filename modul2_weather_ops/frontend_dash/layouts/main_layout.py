import dash_bootstrap_components as dbc
from dash import html, dcc
import yaml
from pathlib import Path
from data_pipeline.weather_client import load_disk_cache

# Load config to get the interval length safely
def get_poll_interval():
    config_path = Path(__file__).parent.parent.parent / 'configs' / 'app_config.yaml'
    try:
        with open(config_path, 'r') as f:
            c = yaml.safe_load(f)
            return c.get('api', {}).get('poll_interval_seconds', 300) * 1000
    except:
        return 300000

def create_main_layout():
    """
    Constructs the main HTML structure of the application using bootstrap components
    and White Glassmorphism conventions.
    """
    layout = dbc.Container([
        # Hidden State Management with pre-warmed Cash
        dcc.Store(id='weather-data-cache', data=load_disk_cache().model_dump()),
        dcc.Interval(
            id='polling-interval',
            interval=get_poll_interval(),
            n_intervals=0 # Trigger immediately 
        ),
        
        # Header Row
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H1("Modul 2 Spatial Weather Platform", className="header-title display-4"),
                    html.P("System Alpha - Real-Time Telemetry Monitor", className="lead text-muted"),
                    html.Div(id="last-updated-text", className="badge bg-primary rounded-pill mt-2 fs-6")
                ], className="glass-panel text-center mt-4")
            ])
        ]),

        # KPI Metrics Row
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div("Highest Temp", className="kpi-label"),
                    html.Div(id="kpi-max-temp", className="kpi-value mt-2", children="--")
                ], className="glass-panel text-center")
            ], width=6),
            dbc.Col([
                html.Div([
                    html.Div("Highest Wind Speed", className="kpi-label"),
                    html.Div(id="kpi-max-wind", className="kpi-value mt-2", children="--")
                ], className="glass-panel text-center")
            ], width=6)
        ]),

        # Spacial Mapping Row
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(
                        id="map-graphic",
                        style={"width": "100%", "aspectRatio": "16/9"},
                        config={"displayModeBar": True, "scrollZoom": True}
                    )
                ], className="glass-panel p-2")
            ])
        ])

    ], fluid=True, className="px-4")

    return layout
