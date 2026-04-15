import dash
import dash_bootstrap_components as dbc
import sys
import os

# Ensure the root of the project is in the PYPATH so we can seamlessly import data_pipeline
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frontend_dash.layouts.main_layout import create_main_layout
from frontend_dash.callbacks.map_callbacks import register_callbacks

# Intialize the app with Dash Bootstrap Components, ignoring their themes since we use custom glassmorphism
# We only load DBC for the grid system natively
app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP, "https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap"],
    suppress_callback_exceptions=True
)

app.title = "System Alpha - Map"

# Inject the layout
app.layout = create_main_layout()

# Register event callbacks
register_callbacks(app)

if __name__ == '__main__':
    # Force port 8050 to avoid any conflict with Taipy (port 5000)
    app.run(debug=True, port=8050)
