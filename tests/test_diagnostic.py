"""
Weather.py Diagnostic Test
==========================
Diagnoses why weather.py main() is returning None
"""

import os
import requests
from dotenv import load_dotenv
from weather import get_lat_lon, get_current_weather, get_forecast_data

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")

print("=" * 70)
print("WEATHER.PY DIAGNOSTIC TEST")
print("=" * 70)

# Test 1: Check if API key exists
print("\n1️⃣  API KEY CHECK:")
if api_key:
    print(f"   ✅ API Key loaded: {api_key[:10]}...{api_key[-5:]}")
else:
    print("   ❌ API Key NOT found in .env file")
    exit(1)

# Test 2: Check geocoding
print("\n2️⃣  GEOCODING TEST:")
city = "London"
state = "10"
country = "GB"
print(f"   Testing: {city}, {state}, {country}")
lat, lon = get_lat_lon(city, state, country, api_key)
if lat and lon:
    print(f"   ✅ Geocoding successful: ({lat}, {lon})")
else:
    print(f"   ❌ Geocoding FAILED: Got ({lat}, {lon})")
    
    # Try alternative geocoding
    print("\n   🔄 Trying simpler geocoding (city only)...")
    lat, lon = get_lat_lon("London", "", "", api_key)
    if lat and lon:
        print(f"   ✅ City-only geocoding successful: ({lat}, {lon})")
    else:
        print(f"   ❌ City-only geocoding FAILED")
        exit(1)

# Test 3: Check current weather
print("\n3️⃣  CURRENT WEATHER TEST:")
print(f"   Fetching weather for ({lat}, {lon})...")
weather_data = get_current_weather(lat, lon, api_key)
if weather_data:
    print(f"   ✅ Current weather retrieved")
    print(f"      Location: {weather_data.name}")
    print(f"      Temp: {weather_data.temperature}°C")
    print(f"      Condition: {weather_data.main}")
else:
    print(f"   ❌ Current weather FAILED")
    exit(1)

# Test 4: Check forecast data
print("\n4️⃣  FORECAST DATA TEST:")
print(f"   Fetching forecasts for ({lat}, {lon})...")
hourly, daily, uv, alerts = get_forecast_data(lat, lon, api_key)
if hourly and daily:
    print(f"   ✅ Forecast data retrieved")
    print(f"      Hourly items: {len(hourly)}")
    print(f"      Daily items: {len(daily)}")
    print(f"      UV Index: {uv}")
else:
    print(f"   ❌ Forecast data FAILED")
    print(f"      Hourly: {len(hourly)} items")
    print(f"      Daily: {len(daily)} items")
    exit(1)

# Test 5: Full main() function
print("\n5️⃣  FULL MAIN() TEST:")
from weather import main
result = main("London", "10", "GB")
if result:
    print(f"   ✅ main() returned successfully")
    print(f"      Type: {type(result).__name__}")
    print(f"      Location: {result.name}")
    print(f"      Temp: {result.temperature}°C")
    print(f"      Hourly forecasts: {len(result.hourly_forecast)}")
    print(f"      Daily forecasts: {len(result.daily_forecast)}")
    print(f"      UV Index: {result.uv_index}")
else:
    print(f"   ❌ main() returned None")

print("\n" + "=" * 70)
print("DIAGNOSTIC COMPLETE")
print("=" * 70)
