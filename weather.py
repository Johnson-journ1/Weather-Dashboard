"""
Weather Data Fetching Module
============================
This module handles all interactions with the OpenWeatherMap API to retrieve
real-time weather data, forecasts, and related information.

Functions:
    - get_lat_lon(): Convert city name to coordinates
    - get_current_weather(): Fetch current weather conditions
    - get_forecast_data(): Fetch hourly and daily forecasts
    - main(): Orchestrate all weather data collection

Author: Weather Dashboard Team
Team Lead: Atitebi Johnson A.  | 2023/12872
Date: January 2026
"""

import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("API_KEY")

# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class WeatherData:
    """
    Data class to store all weather information for a location.
    
    This class represents a complete weather snapshot including current
    conditions, forecasts, and various metrics.
    
    Attributes:
        name (str): City/location name
        main (str): Main weather condition (e.g., "Clear", "Rainy")
        description (str): Detailed weather description
        icon (str): Weather icon code from OpenWeatherMap
        temperature (float): Current temperature in Celsius
        feels_like (float): "Feels like" temperature in Celsius
        humidity (int): Relative humidity percentage (0-100)
        pressure (int): Atmospheric pressure in millibars
        wind_speed (float): Wind speed in meters per second
        visibility (int): Visibility distance in meters
        uv_index (float): UV index value (0-11+)
        hourly_forecast (list): List of dicts with hourly predictions (24 hours)
        daily_forecast (list): List of dicts with daily predictions (5-7 days)
        alerts (list): List of active weather alerts/warnings
        timezone (str): Timezone identifier for the location (e.g., "Europe/London")
        timezone_offset (int): UTC offset in seconds (e.g., 3600 for UTC+1)
        sunrise (int): Unix timestamp of sunrise time
        sunset (int): Unix timestamp of sunset time
        last_updated (int): Unix timestamp when data was last fetched
    """
    name: str
    main: str
    description: str
    icon: str
    temperature: float
    feels_like: float
    humidity: int
    pressure: int
    wind_speed: float
    visibility: int
    uv_index: float
    hourly_forecast: list
    daily_forecast: list
    alerts: list
    timezone: str = "UTC"
    timezone_offset: int = 0
    sunrise: int = 0
    sunset: int = 0
    last_updated: int = 0

# ============================================================================
# API FUNCTIONS
# ============================================================================

def get_lat_lon(city_name, state_code="", country_code="", api_key=None):
    """
    Convert city name to geographic coordinates (latitude, longitude).
    
    This function uses OpenWeatherMap's Geocoding API to convert a city name
    into its corresponding latitude and longitude coordinates. These coordinates
    are then used to fetch weather data for that location.
    
    API Endpoint: /geo/1.0/direct
    
    Args:
        city_name (str): Name of the city (e.g., "London")
        state_code (str, optional): ISO 3166-1 state code (e.g., "10" for England). Defaults to "".
        country_code (str, optional): ISO 3166-1 country code (e.g., "GB" for UK). Defaults to "".
        api_key (str, optional): OpenWeatherMap API key. Defaults to None (uses env variable).
    
    Returns:
        tuple: (latitude, longitude) if successful, (None, None) if failed
        
    Example:
        >>> lat, lon = get_lat_lon("London", "10", "GB", api_key)
        >>> print(lat, lon)
        51.5085 -0.1257
    """
    # Use global api_key if not provided
    if api_key is None:
        api_key = globals()['api_key']
    
    # Build location string based on provided parameters
    location = city_name
    if state_code:
        location += f",{state_code}"
    if country_code:
        location += f",{country_code}"
    
    # Construct API URL with city information (using Geocoding API)
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&appid={api_key}"
    
    # Make API request
    response = requests.get(url)
    
    # Check if request was successful
    if response.status_code == 200:
        data = response.json()
        # Check if results were found
        if data and len(data) > 0:
            # Extract coordinates from first result
            lat = data[0]["lat"]
            lon = data[0]["lon"]
            return lat, lon
    
    # Return None values if API call fails or no results found
    return None, None

def get_current_weather(lat, lon, api_key):
    """
    Fetch current weather conditions for a given location.
    
    Uses OpenWeatherMap's Current Weather API to retrieve real-time weather
    data including temperature, humidity, wind speed, and more.
    
    API Endpoint: /data/2.5/weather
    
    Args:
        lat (float): Latitude coordinate
        lon (float): Longitude coordinate
        api_key (str): OpenWeatherMap API key
    
    Returns:
        WeatherData: Object containing current weather information
        None: If API request fails
        
    Data Retrieved:
        - Temperature and "feels like" temperature
        - Weather description and icon
        - Humidity, pressure, wind speed, visibility
    """
    # Construct API URL with coordinates
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    
    # Make API request
    response = requests.get(url)
    
    # Check if request was successful
    if response.status_code == 200:
        data = response.json()
        
        # Create WeatherData object with API response data
        weather_data = WeatherData(
            name=data.get("name"),
            main=data["weather"][0]["main"],
            description=data["weather"][0]["description"],
            icon=data["weather"][0]["icon"],
            temperature=int(data["main"]["temp"]),
            feels_like=int(data["main"].get("feels_like", 0)),
            humidity=int(data["main"].get("humidity", 0)),
            pressure=int(data["main"].get("pressure", 0)),
            wind_speed=int(data.get("wind", {}).get("speed", 0)),
            visibility=data.get("visibility", 0),
            uv_index=0,  # Will be populated by get_forecast_data()
            hourly_forecast=[],  # Will be populated by get_forecast_data()
            daily_forecast=[],  # Will be populated by get_forecast_data()
            alerts=[],  # Will be populated by get_forecast_data()
            timezone=data.get("sys", {}).get("country", "UTC"),  # Country code from API
            timezone_offset=data.get("timezone", 0),  # UTC offset in seconds from API
            sunrise=data.get("sys", {}).get("sunrise", 0),  # Unix timestamp
            sunset=data.get("sys", {}).get("sunset", 0),  # Unix timestamp
            last_updated=int(datetime.now().timestamp())  # Current time
        )
        return weather_data
    else:
        # Return None if API call fails
        return None

#print(get_lat_lon("London", "10", "GB", api_key))

def get_forecast_data(lat, lon, api_key):
    """
    Fetch hourly and daily forecast data using the 5-Day Forecast API.

    Uses OpenWeatherMap's 5-day/3-hour forecast API (available on free tier)
    to retrieve weather predictions. Also fetches UV index from a separate
    endpoint.

    API Endpoints:
        - /data/2.5/forecast (5-day forecast with 3-hour intervals)
        - /data/2.5/uvi (UV index)

    Args:
        lat (float): Latitude coordinate
        lon (float): Longitude coordinate
        api_key (str): OpenWeatherMap API key

    Returns:
        tuple: (hourly_forecast, daily_forecast, uv_index, alerts)
               - hourly_forecast (list): 8 items × 3 hours = 24-hour forecast
               - daily_forecast (list): Up to 5-6 daily forecasts (API limit)
               - uv_index (float): Current UV index value
               - alerts (list): Empty list (alerts not available on free tier)
    """
    # Use the 5-day/3-hour forecast API which is available on free tier
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Extract city timezone offset (seconds) if available
        timezone_offset = data.get('city', {}).get('timezone', 0)

        # Get hourly forecast (next 24 hours - every 3 hours from API)
        hourly_forecast = []
        for i, item in enumerate(data.get("list", [])):
            if i >= 8:  # 8 items * 3 hours = 24 hours
                break
            hourly_forecast.append({
                "time": item.get("dt"),
                "temp": item.get("main", {}).get("temp"),
                "icon": item["weather"][0].get("icon"),
                "description": item["weather"][0].get("description"),
                "precipitation": item.get("pop", 0) * 100,
                "humidity": item.get("main", {}).get("humidity", 0)
            })

        # Build daily forecast by aggregating 3-hour entries into calendar days
        from collections import defaultdict
        daily_buckets = defaultdict(list)

        for item in data.get('list', []):
            ts = item.get('dt')
            # Convert to location-local date using timezone offset
            utc_dt = datetime.fromtimestamp(ts, tz=timezone.utc).replace(tzinfo=None)
            local_dt = utc_dt + timedelta(seconds=timezone_offset)
            local_date = local_dt.date()
            daily_buckets[local_date].append((local_dt, item))

        # For each day, compute sensible aggregates
        daily_forecast = []
        for local_date in sorted(daily_buckets.keys()):
            entries = daily_buckets[local_date]
            temps = []
            pops = []
            humidities = []
            wind_speeds = []
            # pick a representative entry (closest to local noon if possible)
            rep_entry = None
            rep_dt = None
            best_noon_diff = None

            for local_dt, item in entries:
                main = item.get('main', {})
                # Collect all temperatures throughout the day
                temps.append(main.get('temp', 0))
                pops.append(item.get('pop', 0) * 100)
                humidities.append(main.get('humidity', 0))
                wind_speeds.append(item.get('wind', {}).get('speed', 0))

                # prefer entry at 12:00 local time
                noon = local_dt.replace(hour=12, minute=0, second=0, microsecond=0)
                diff = abs((local_dt - noon).total_seconds())
                if best_noon_diff is None or diff < best_noon_diff:
                    best_noon_diff = diff
                    rep_entry = item
                    rep_dt = local_dt

            # Fallback to first entry if none selected
            if rep_entry is None:
                rep_dt, rep_entry = entries[0]

            # Build daily summary
            try:
                temp_max_val = max([t for t in temps if t is not None])
            except ValueError:
                temp_max_val = None
            try:
                temp_min_val = min([t for t in temps if t is not None])
            except ValueError:
                temp_min_val = None

            daily_forecast.append({
                "time": int(rep_dt.timestamp()),
                "temp_max": temp_max_val,
                "temp_min": temp_min_val,
                "icon": rep_entry["weather"][0].get("icon"),
                "description": rep_entry["weather"][0].get("description"),
                "humidity": int(sum(humidities)/len(humidities)) if humidities else None,
                "wind_speed": float(max(wind_speeds)) if wind_speeds else 0,
                "precipitation": float(max(pops)) if pops else 0
            })

            # No artificial limit - get all available days from API (typically 5-6 days)

        # Get UV index (using separate UV API endpoint)
        # Include current timestamp to get actual current UV, not default noon value
        # Note: OpenWeatherMap free tier API returns the DAILY MAXIMUM UV index,
        # not the instantaneous UV at the request time. This is by design to show
        # users the worst-case UV exposure they should prepare for during the day.
        uv_index = 0
        current_timestamp = int(datetime.now().timestamp())
        uv_url = f"https://api.openweathermap.org/data/2.5/uvi?lat={lat}&lon={lon}&dt={current_timestamp}&appid={api_key}"
        uv_response = requests.get(uv_url)
        if uv_response.status_code == 200:
            uv_index = uv_response.json().get("value", 0)

        return hourly_forecast, daily_forecast, uv_index, []
    else:
        return [], [], 0, []

def main(city_name, state_name="", country_code=""):
    """
    Orchestrate the complete weather data collection process.
    
    This is the main function that coordinates all API calls and combines
    the results into a single WeatherData object.
    
    Args:
        city_name (str): Name of the city to get weather for (required)
        state_name (str, optional): State/province code. Defaults to "".
        country_code (str, optional): Country code. Defaults to "".
    
    Returns:
        WeatherData: Complete weather information object
        
    Examples:
        >>> # Just city name
        >>> weather = main("London")
        
        >>> # City with country code
        >>> weather = main("London", "", "GB")
        
        >>> # City, state, and country
        >>> weather = main("London", "10", "GB")
    """
    # Step 1: Convert city name to coordinates
    lat, lon = get_lat_lon(city_name, state_name, country_code, api_key)
    
    if lat is not None and lon is not None:
        # Step 2: Fetch current weather
        weather_datas = get_current_weather(lat, lon, api_key)
        
        # Step 3: Fetch forecasts and UV index
        hourly, daily, uv, alerts = get_forecast_data(lat, lon, api_key)
        
        # Step 4: Populate the WeatherData object with all data
        if weather_datas:
            weather_datas.hourly_forecast = hourly
            weather_datas.daily_forecast = daily
            weather_datas.uv_index = uv
            weather_datas.alerts = alerts
        
        return weather_datas
    else:
        # Geocoding failed - city/location not found
        print(f"❌ Error: Could not find coordinates for '{city_name}'")
        if state_name:
            print(f"   Hint: Try without state code '{state_name}'")
        return None

if __name__ == "__main__":
    """
    Test the weather data fetching when running this module directly.
    """
    weather_datas = main("London", "10", "GB")
    print(weather_datas)