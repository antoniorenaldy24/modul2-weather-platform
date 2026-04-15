from data_pipeline.weather_client import fetch_live_weather, load_disk_cache
from data_pipeline.geo_transformers import collection_to_dataframe, generate_plotly_map
import threading
import time
import yaml
from pathlib import Path

# --- GLOBAL STATE VARIABLES (Bound to Taipy GUI) ---
import plotly.graph_objects as go

# Pre-Warming the GUI variables using synchronous disk cache read
_cached = load_disk_cache()
_df_cached = collection_to_dataframe(_cached)

if _df_cached.empty:
    fig = go.Figure()
    fig.update_layout(title="Awaiting Telemetry Data...", template="plotly_white", mapbox_style="carto-positron")
    kpi_temp = "--"
    kpi_wind = "--"
    status_text = "Initializing Platform..."
else:
    fig = generate_plotly_map(_df_cached)
    kpi_temp = f"{_df_cached.loc[_df_cached['temperature_c'].idxmax(), 'temperature_c']}°C ({_df_cached.loc[_df_cached['temperature_c'].idxmax(), 'city_name']})"
    kpi_wind = f"{_df_cached.loc[_df_cached['wind_speed_kmh'].idxmax(), 'wind_speed_kmh']} km/h ({_df_cached.loc[_df_cached['wind_speed_kmh'].idxmax(), 'city_name']})"
    status_text = f"Last Cached: {_cached.last_updated.strftime('%Y-%m-%d %H:%M:%S')} (⚠️ USING LOCAL CACHE)"

def _fetch_interval():
    config_path = Path(__file__).parent.parent.parent / 'configs' / 'app_config.yaml'
    try:
        with open(config_path, 'r') as f:
            c = yaml.safe_load(f)
            return c.get('api', {}).get('poll_interval_seconds', 300)
    except:
        return 300

POLL_INTERVAL = _fetch_interval()

def update_global_state_from_api(state):
    """
    Called by the GUI periodic interval to mutate the bound state safely.
    Hits the pipeline, computes variables, overwrites state.
    """
    collection = fetch_live_weather()
    df = collection_to_dataframe(collection)
    
    # 1. Update the chart
    new_fig = generate_plotly_map(df)
    state.fig = new_fig
    
    # 2. Update KPI metrics
    if not df.empty:
        highest_temp_idx = df['temperature_c'].idxmax()
        highest_wind_idx = df['wind_speed_kmh'].idxmax()
        
        state.kpi_temp = f"{df.loc[highest_temp_idx, 'temperature_c']}°C ({df.loc[highest_temp_idx, 'city_name']})"
        state.kpi_wind = f"{df.loc[highest_wind_idx, 'wind_speed_kmh']} km/h ({df.loc[highest_wind_idx, 'city_name']})"
    
    # 3. Update Sync Status
    last_updated_str = collection.last_updated.strftime("%Y-%m-%d %H:%M:%S")
    indicator = f"Last API Fetch: {last_updated_str}"
    if collection.is_cached_fallback:
        indicator += " (⚠️ CACHED/FALLBACK)"
    state.status_text = indicator


def background_fetcher(gui):
    """
    Runs in a dedicated thread. Periodically triggers Taipy's state update handler.
    To prevent cross-thread issues, we use invoke_callback allowing the main thread to do the actual data binding.
    """
    # Sleep gently until app warms up
    time.sleep(2)
    while True:
        # Request GUI to execute our handler with its state context
        try:
            gui.invoke_callback(gui, update_global_state_from_api)
        except Exception as e:
            print(f"Taipy background fetch error: {e}")
        
        time.sleep(POLL_INTERVAL)
