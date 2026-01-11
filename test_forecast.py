from weather import main

result = main('London', '10', 'GB')

print("=" * 60)
print("24-HOUR FORECAST")
print("=" * 60)
print(f"Total items: {len(result.hourly_forecast)}")
for h in result.hourly_forecast:
    from datetime import datetime
    time_str = datetime.fromtimestamp(h['time']).strftime('%Y-%m-%d %H:%M')
    print(f"  {time_str}: {h['temp']}°C - {h['description']} ({h['precipitation']:.0f}% chance of rain)")

print("\n" + "=" * 60)
print("7-DAY FORECAST")
print("=" * 60)
print(f"Total items: {len(result.daily_forecast)}")
for d in result.daily_forecast:
    from datetime import datetime
    time_str = datetime.fromtimestamp(d['time']).strftime('%Y-%m-%d')
    print(f"  {time_str}: {d['temp_max']}°C / {d['temp_min']}°C - {d['description']} (💨 {d['wind_speed']:.1f} m/s, 💧 {d['humidity']}%)")

print("\n" + "=" * 60)
print("ADDITIONAL METRICS")
print("=" * 60)
print(f"Wind Speed: {result.wind_speed} m/s")
print(f"Visibility: {result.visibility} m ({result.visibility/1000:.1f} km)")
print(f"Humidity: {result.humidity}%")
print(f"UV Index: {result.uv_index}")
