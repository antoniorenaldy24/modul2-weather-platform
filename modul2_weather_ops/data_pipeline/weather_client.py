import requests
import logging
import yaml
import json
import os
import tempfile
from pathlib import Path
from pydantic import ValidationError
from .schemas import WeatherCollection, WeatherPoint

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

CONFIG_PATH = Path(__file__).parent.parent / 'configs' / 'app_config.yaml'
CACHE_PATH = Path(__file__).parent.parent / 'temp_db' / 'latest_weather.json'

def load_config() -> dict:
    try:
        with open(CONFIG_PATH, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        return {}

def load_disk_cache() -> WeatherCollection:
    """Reads the JSON cache disk on boot to provide zero-load time."""
    if CACHE_PATH.exists():
        try:
            with open(CACHE_PATH, 'r') as f:
                data = json.load(f)
                return WeatherCollection(**data)
        except Exception as e:
            logger.error(f"Cache read error: {e}")
            
    # Return empty collection if nothing exists yet
    return WeatherCollection(is_cached_fallback=True)

def save_disk_cache(collection: WeatherCollection):
    """Saves the validated Pydantic model to JSON using atomic write."""
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True) # Ensure temp_db exists
    
    # Atomic file write to prevent UI dash/taipy encountering partial reads/race conditions
    tmp_path = CACHE_PATH.with_suffix('.tmp')
    try:
        with open(tmp_path, 'w') as f:
            json.dump(collection.model_dump(mode='json'), f)
        os.replace(tmp_path, CACHE_PATH) 
    except Exception as e:
        logger.error(f"Failed to save atomic cache: {e}")

def fetch_live_weather(fallback_cache: WeatherCollection = None) -> WeatherCollection:
    """
    BULK QUERY IMPLEMENTATION.
    Requests all target coordinates in a single array payload for maximum speed.
    """
    config = load_config()
    endpoint = config.get('api', {}).get('open_meteo_endpoint', 'https://api.open-meteo.com/v1/forecast')
    timeout = config.get('api', {}).get('timeout_seconds', 30)
    targets = config.get('target_coordinates', {})
    
    if not targets:
        return fallback_cache if fallback_cache else WeatherCollection(is_cached_fallback=True)

    city_names = list(targets.keys())
    lats = [str(targets[city]['lat']) for city in city_names]
    lons = [str(targets[city]['lon']) for city in city_names]
    
    try:
        # BULK Querying 
        params = {
            "latitude": ",".join(lats),
            "longitude": ",".join(lons),
            "current": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m"]
        }
        
        response = requests.get(endpoint, params=params, timeout=timeout)
        response.raise_for_status() 
        data_arrays = response.json()
        
        # If there's only 1 target, open-meteo returns a single obj, NOT an array. So we normalize to array:
        if isinstance(data_arrays, dict):
            data_arrays = [data_arrays]
            
        points = []
        for index, data in enumerate(data_arrays):
            current = data.get("current", {})
            point = WeatherPoint(
                city_name=city_names[index],
                lat=targets[city_names[index]]['lat'],
                lon=targets[city_names[index]]['lon'],
                temperature_c=current.get("temperature_2m", 0.0),
                humidity=current.get("relative_humidity_2m", 0.0),
                wind_speed_kmh=current.get("wind_speed_10m", 0.0)
            )
            points.append(point)
            
        logger.info(f"Successfully BULK fetched telemetry for {len(points)} locations.")
        res_collection = WeatherCollection(points=points, is_cached_fallback=False)
        
        # Save cache dynamically
        save_disk_cache(res_collection)
        return res_collection
        
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Network Error: {req_err}")
    except Exception as e:
        logger.error(f"Bulk weather fetch error: {e}")
        
    # Degrade Gracefully
    logger.warning("Degrading gracefully. Checking prior memories...")
    
    # Try reading the persistent cache
    existing_cache = load_disk_cache()
    if existing_cache and existing_cache.points:
        logger.info("Serving from local disk `.json` cache.")
        existing_cache.is_cached_fallback = True
        return existing_cache
        
    return fallback_cache if fallback_cache else WeatherCollection(points=[], is_cached_fallback=True)
