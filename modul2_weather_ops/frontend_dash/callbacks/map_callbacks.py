from dash import Output, Input, State, dcc
import pandas as pd

from data_pipeline.weather_client import fetch_live_weather
from data_pipeline.geo_transformers import collection_to_dataframe, generate_plotly_map

def register_callbacks(app):
    """
    Registers the unidirectional state flow callbacks for the Dash map.
    """
    
    @app.callback(
        Output('weather-data-cache', 'data'),
        Input('polling-interval', 'n_intervals')
    )
    def trigger_api_fetch(n_intervals):
        """
        Rule 12: Triggered periodically. Fetches API and stores to cache.
        Returns the data as a serialized python dict for dcc.Store.
        """
        # Fetch data securely via the resilient Brain pipeline
        collection = fetch_live_weather()
        # Convert schema to dict so dash can serialize it
        return collection.model_dump()

    @app.callback(
        [Output('map-graphic', 'figure'),
         Output('last-updated-text', 'children'),
         Output('kpi-max-temp', 'children'),
         Output('kpi-max-wind', 'children')],
        [Input('weather-data-cache', 'data')]
    )
    def render_map_from_cache(cached_data):
        """
        Rule 15: Purely reactive map rendering function.
        Does NOT hit the API directly. Triggers when the cache dict updates.
        """
        if not cached_data or 'points' not in cached_data:
            from plotly import graph_objects as go
            return go.Figure(), "Awaiting data...", "--", "--"
            
        # Re-initialize collection from the serialized dict
        from data_pipeline.schemas import WeatherCollection
        collection = WeatherCollection(**cached_data)
        
        # Transform via Geo Transformers
        df = collection_to_dataframe(collection)
        fig = generate_plotly_map(df)
        
        # Calculate KPIs
        last_updated_str = collection.last_updated.strftime("%Y-%m-%d %H:%M:%S")
        status_str = f"Last API Fetch: {last_updated_str}"
        if collection.is_cached_fallback:
            status_str += " (⚠️ USING CACHED FALLBACK)"
            
        max_temp = "--"
        max_wind = "--"
        
        if not df.empty:
            highest_temp_idx = df['temperature_c'].idxmax()
            highest_wind_idx = df['wind_speed_kmh'].idxmax()
            
            max_temp_val = df.loc[highest_temp_idx, 'temperature_c']
            max_temp_city = df.loc[highest_temp_idx, 'city_name']
            max_temp = f"{max_temp_val}°C ({max_temp_city})"
            
            max_wind_val = df.loc[highest_wind_idx, 'wind_speed_kmh']
            max_wind_city = df.loc[highest_wind_idx, 'city_name']
            max_wind = f"{max_wind_val} km/h ({max_wind_city})"
            
        return fig, status_str, max_temp, max_wind
