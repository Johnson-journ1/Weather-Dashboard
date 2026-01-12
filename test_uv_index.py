"""
UV Index Verification Script
=============================
This script fetches and displays UV index data from OpenWeatherMap
to help verify if the values are accurate or inflated.
"""

import os
import requests
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")

def get_uv_index_data(lat, lon):
    """
    Fetch UV index data and related metrics from OpenWeatherMap.
    
    Args:
        lat (float): Latitude
        lon (float): Longitude
    
    Returns:
        dict: UV index data with additional context
    """
    print(f"\n{'='*70}")
    print(f"UV INDEX VERIFICATION - Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}\n")
    
    # Get current UV index WITH CURRENT TIMESTAMP
    current_timestamp = int(datetime.now().timestamp())
    uv_url = f"https://api.openweathermap.org/data/2.5/uvi?lat={lat}&lon={lon}&dt={current_timestamp}&appid={api_key}"
    print(f"📍 Fetching UV data for: Latitude {lat}, Longitude {lon}\n")
    
    try:
        uv_response = requests.get(uv_url)
        if uv_response.status_code == 200:
            uv_data = uv_response.json()
            current_uv = uv_data.get("value", 0)
            
            print(f"Current UV Index: {current_uv}")
            print(f"Full API Response: {uv_data}\n")
            
            # Get current weather to check sun position
            weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
            weather_response = requests.get(weather_url)
            
            if weather_response.status_code == 200:
                weather_data = weather_response.json()
                clouds = weather_data.get("clouds", {}).get("all", 0)
                sunrise = weather_data.get("sys", {}).get("sunrise", 0)
                sunset = weather_data.get("sys", {}).get("sunset", 0)
                
                sunrise_time = datetime.fromtimestamp(sunrise).strftime('%H:%M:%S')
                sunset_time = datetime.fromtimestamp(sunset).strftime('%H:%M:%S')
                current_time = datetime.now()
                
                print(f"☀️  Sunrise: {sunrise_time}")
                print(f"🌅 Sunset: {sunset_time}")
                print(f"☁️  Cloud Coverage: {clouds}%")
                print(f"🕐 Current Time: {current_time.strftime('%H:%M:%S')}\n")
                
                # UV Index Scale Reference
                print(f"{'='*70}")
                print("UV INDEX SCALE REFERENCE:")
                print(f"{'='*70}")
                print("0-2:   Low       ☀️  Minimal protection needed")
                print("3-5:   Moderate  ⚠️  Wear sunscreen SPF 30+")
                print("6-7:   High      ⚠️⚠️ Seek shade during midday")
                print("8-10:  Very High ⚠️⚠️⚠️ Avoid sun exposure 10am-4pm")
                print("11+:   Extreme   🚨 Avoid all sun exposure")
                print(f"\n{'='*70}\n")
                
                # Classify current UV
                if current_uv <= 2:
                    classification = "LOW"
                    emoji = "☀️"
                elif current_uv <= 5:
                    classification = "MODERATE"
                    emoji = "⚠️"
                elif current_uv <= 7:
                    classification = "HIGH"
                    emoji = "⚠️⚠️"
                elif current_uv <= 10:
                    classification = "VERY HIGH"
                    emoji = "⚠️⚠️⚠️"
                else:
                    classification = "EXTREME"
                    emoji = "🚨"
                
                print(f"CURRENT UV INDEX ASSESSMENT:")
                print(f"Value: {current_uv} → {classification} {emoji}")
                print(f"\nFactors affecting UV index:")
                print(f"  • Cloud coverage: {clouds}% (reduces UV by ~{clouds*0.5:.0f}%)")
                print(f"  • Time of day: {current_time.strftime('%H:%M')} (strongest 10am-4pm)")
                print(f"  • Season: {datetime.now().strftime('%B')} (Jan-Feb are winter in NH)")
                
                # Estimate expected range for time of day
                hour = current_time.hour
                if 6 <= hour <= 9:
                    expected_range = "LOW (morning)"
                elif 10 <= hour <= 16:
                    expected_range = "MODERATE-HIGH (midday)"
                elif 17 <= hour <= 19:
                    expected_range = "MODERATE (afternoon)"
                else:
                    expected_range = "VERY LOW (sunrise/sunset/night)"
                
                print(f"\nExpected UV range for this time: {expected_range}")
                
                if current_uv > 8 and hour not in range(10, 17):
                    print(f"\n⚠️  WARNING: UV index seems unusually high for {current_time.strftime('%H:%M')}")
                    print(f"    Verify the data or check if API is returning max daily UV instead of current.")
                
            return uv_data
        else:
            print(f"❌ Error fetching UV data: {uv_response.status_code}")
            return None
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def main():
    """Main function to run UV index verification."""
    
    # Example: Lagos, Nigeria coordinates (can be changed)
    print("\n🌍 UV Index Verification Tool\n")
    print("Instructions:")
    print("1. Enter a city name, OR")
    print("2. Enter latitude and longitude directly\n")
    
    user_choice = input("Enter city name or press 'Enter' for custom coordinates: ").strip()
    
    if user_choice:
        # Geocode the city
        from weather import get_lat_lon
        try:
            coords = get_lat_lon(user_choice)
            if coords:
                lat, lon = coords
                print(f"\n✓ Found coordinates: {lat}, {lon}")
            else:
                print(f"\n❌ Could not find coordinates for '{user_choice}'")
                return
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return
    else:
        # Get custom coordinates
        try:
            lat = float(input("Enter latitude: "))
            lon = float(input("Enter longitude: "))
        except ValueError:
            print("❌ Invalid coordinates")
            return
    
    # Fetch and display UV index
    get_uv_index_data(lat, lon)

if __name__ == "__main__":
    main()
