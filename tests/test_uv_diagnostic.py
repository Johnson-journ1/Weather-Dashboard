"""
Advanced UV Index Diagnostic
============================
Tests multiple API variations to understand how OpenWeatherMap UV API works
"""

import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
api_key = os.getenv("API_KEY")

def test_uv_variations():
    """Test different UV API call variations"""
    
    lat, lon = 6.5960605, 3.340787  # Ikeja, Nigeria
    current_time = datetime.now()
    current_ts = int(current_time.timestamp())
    
    print(f"\n{'='*70}")
    print(f"UV INDEX API DIAGNOSTIC TEST")
    print(f"Current UTC Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print(f"Current Local Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Location: Ikeja, Nigeria ({lat}, {lon})")
    print(f"{'='*70}\n")
    
    # Test 1: Without dt parameter (original)
    print("TEST 1: WITHOUT dt parameter")
    print("-" * 70)
    url1 = f"https://api.openweathermap.org/data/2.5/uvi?lat={lat}&lon={lon}&appid={api_key}"
    r1 = requests.get(url1)
    if r1.status_code == 200:
        data1 = r1.json()
        returned_time = datetime.utcfromtimestamp(data1.get('date', 0))
        print(f"URL: /data/2.5/uvi (no dt)")
        print(f"Response date: {returned_time.strftime('%Y-%m-%d %H:%M:%S')} UTC")
        print(f"UV Value: {data1.get('value', 0)}")
    print()
    
    # Test 2: With current dt parameter
    print("TEST 2: WITH current timestamp in dt parameter")
    print("-" * 70)
    url2 = f"https://api.openweathermap.org/data/2.5/uvi?lat={lat}&lon={lon}&dt={current_ts}&appid={api_key}"
    r2 = requests.get(url2)
    if r2.status_code == 200:
        data2 = r2.json()
        returned_time = datetime.utcfromtimestamp(data2.get('date', 0))
        print(f"URL: /data/2.5/uvi?dt={current_ts}")
        print(f"Requested timestamp: {datetime.utcfromtimestamp(current_ts).strftime('%Y-%m-%d %H:%M:%S')} UTC")
        print(f"Response date: {returned_time.strftime('%Y-%m-%d %H:%M:%S')} UTC")
        print(f"UV Value: {data2.get('value', 0)}")
    print()
    
    # Test 3: With historical dt (6 hours ago)
    print("TEST 3: WITH historical timestamp (6 hours ago)")
    print("-" * 70)
    past_ts = int((datetime.now() - timedelta(hours=6)).timestamp())
    url3 = f"https://api.openweathermap.org/data/2.5/uvi?lat={lat}&lon={lon}&dt={past_ts}&appid={api_key}"
    r3 = requests.get(url3)
    if r3.status_code == 200:
        data3 = r3.json()
        returned_time = datetime.utcfromtimestamp(data3.get('date', 0))
        print(f"URL: /data/2.5/uvi?dt={past_ts}")
        print(f"Requested timestamp: {datetime.utcfromtimestamp(past_ts).strftime('%Y-%m-%d %H:%M:%S')} UTC (6h ago)")
        print(f"Response date: {returned_time.strftime('%Y-%m-%d %H:%M:%S')} UTC")
        print(f"UV Value: {data3.get('value', 0)}")
    print()
    
    # Test 4: With future dt (noon today)
    print("TEST 4: WITH noon UTC timestamp (peak expected)")
    print("-" * 70)
    noon_utc = datetime.utcnow().replace(hour=12, minute=0, second=0, microsecond=0)
    noon_ts = int(noon_utc.timestamp())
    url4 = f"https://api.openweathermap.org/data/2.5/uvi?lat={lat}&lon={lon}&dt={noon_ts}&appid={api_key}"
    r4 = requests.get(url4)
    if r4.status_code == 200:
        data4 = r4.json()
        returned_time = datetime.utcfromtimestamp(data4.get('date', 0))
        print(f"URL: /data/2.5/uvi?dt={noon_ts}")
        print(f"Requested timestamp: {noon_utc.strftime('%Y-%m-%d %H:%M:%S')} UTC (noon UTC)")
        print(f"Response date: {returned_time.strftime('%Y-%m-%d %H:%M:%S')} UTC")
        print(f"UV Value: {data4.get('value', 0)}")
    print()
    
    # Analysis
    print(f"{'='*70}")
    print("ANALYSIS:")
    print(f"{'='*70}\n")
    
    if r1.status_code == 200:
        val1 = r1.json().get('value', 0)
    if r2.status_code == 200:
        val2 = r2.json().get('value', 0)
    
    if val1 == val2:
        print("⚠️  FINDING: Values are IDENTICAL regardless of dt parameter!")
        print("    This suggests OpenWeatherMap returns the DAILY MAX UV")
        print("    NOT the instantaneous UV at the requested time.")
        print("\n    Possible interpretations:")
        print("    1. The free API tier doesn't support time-specific UV queries")
        print("    2. The API always returns daily max (safest for user guidance)")
        print("    3. Historical/future UV forecasts aren't available on free tier")
    else:
        print("✓ Values differ with different timestamps!")
        print(f"  Current time UV: {val2}")
        print(f"  Default time UV: {val1}")

if __name__ == "__main__":
    test_uv_variations()
