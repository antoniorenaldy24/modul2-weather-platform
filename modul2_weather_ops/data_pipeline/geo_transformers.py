import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from .schemas import WeatherCollection

def collection_to_dataframe(collection: WeatherCollection) -> pd.DataFrame:
    """
    Transforms the Pydantic WeatherCollection into a flattened Pandas DataFrame.
    This DataFrame is structure-agnostic, usable by both Dash and Taipy.
    
    Args:
        collection (WeatherCollection): Validated points.
        
    Returns:
        pd.DataFrame: Contains lat, lon, city, and telemetry properties.
    """
    if not collection.points:
        return pd.DataFrame(columns=[
            'city_name', 'lat', 'lon', 'temperature_c', 'wind_speed_kmh', 'humidity', 'timestamp'
        ])
    
    data = [point.model_dump() for point in collection.points]
    df = pd.DataFrame(data)
    return df

def generate_plotly_map(df: pd.DataFrame) -> go.Figure:
    """
    Generates a Plotly Mapbox using the transformed DataFrame.
    Abstracted here so both System Alpha and System Beta can utilize identical logic.
    
    Args:
        df (pd.DataFrame): telemetry dataframe.
        
    Returns:
        go.Figure: Mapbox visualization ready for the UI.
    """
    if df.empty:
        # Return empty generic figure
        fig = go.Figure()
        fig.update_layout(title="Awaiting Telemetry Data...", template="plotly_white")
        return fig
        
    # Plotly Express Scatter Mapbox
    fig = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lon",
        hover_name="city_name",
        hover_data={"temperature_c": True, "humidity": True, "wind_speed_kmh": True},
        color="temperature_c",
        color_continuous_scale=px.colors.sequential.Inferno,
        size="wind_speed_kmh", 
        zoom=4.0,
        center={"lat": -0.789, "lon": 113.921}, # Center of Indonesia roughly
        title="Live Weather Telemetry",
        labels={
            "temperature_c": "Suhu (°C)",
            "humidity": "Kelembapan (%)",
            "wind_speed_kmh": "Kecepatan Angin (km/jam)",
            "lat": "Garis Lintang",
            "lon": "Garis Bujur",
            "city_name": "Kota"
        }
    )
    
    fig.update_layout(
        template="plotly_white",
        margin={"r":0,"t":40,"l":0,"b":0},
        uirevision='constant' # Rule 71: Prevent re-zoom on refresh
    )
    
    # Override mapbox style to light theme
    fig.update_layout(mapbox_style="carto-positron")
    
    return fig
