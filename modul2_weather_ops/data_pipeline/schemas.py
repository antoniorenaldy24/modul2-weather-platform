from datetime import datetime
from pydantic import BaseModel, Field

class WeatherPoint(BaseModel):
    """
    Pydantic schema representing a single geography point's weather.
    Ensures validation of dynamic fields before map rendering.
    """
    city_name: str
    lat: float
    lon: float
    temperature_c: float = Field(..., description="Temperature in Celsius")
    wind_speed_kmh: float = Field(..., description="Wind speed in km/h")
    humidity: float = Field(..., description="Relative humidity percentage")
    timestamp: datetime = Field(default_factory=datetime.now)

class WeatherCollection(BaseModel):
    """
    Collection model acting as a defensive boundary for the entire map's data load.
    Will safely degenerate to the last cached state or an empty list.
    """
    points: list[WeatherPoint] = []
    last_updated: datetime = Field(default_factory=datetime.now)
    is_cached_fallback: bool = False
