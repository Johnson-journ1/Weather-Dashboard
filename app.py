"""
Weather Dashboard Flask Application
===================================
This module creates a Flask web application that displays real-time weather data
and forecasts using the OpenWeatherMap API.

Author: Weather Dashboard Team
Date: January 2026
"""

from flask import Flask, render_template, request
from weather import main as get_weather_data
from datetime import datetime, timedelta

# Initialize Flask application
app = Flask(__name__)

# ============================================================================
# CUSTOM JINJA2 FILTERS
# ============================================================================

@app.template_filter('strftime')
def strftime_filter(timestamp, format_string):
    """
    Convert Unix timestamp to formatted date string.
    
    This custom Jinja2 filter allows templates to format Unix timestamps
    into human-readable date and time strings.
    
    Args:
        timestamp (int): Unix timestamp (seconds since epoch)
        format_string (str): Format string with custom placeholders:
                           - '%a, %b %d' for "Mon, Jan 01"
                           - '%H:%M' for "14:30"
                           - '%Y-%m-%d %H:%M' for "2026-01-11 14:30"
    
    Returns:
        str: Formatted date/time string
        
    Example:
        {{ timestamp | strftime('%H:%M') }} → "14:30"
    """
    try:
        # Convert Unix timestamp to datetime object
        dt = datetime.fromtimestamp(timestamp)
        
        # Map custom format strings to Python strftime format codes
        format_map = {
            '%a, %b %d': '%a, %b %d',
            '%H:%M': '%H:%M',
            '%Y-%m-%d %H:%M': '%Y-%m-%d %H:%M'
        }
        actual_format = format_map.get(format_string, format_string)
        
        return dt.strftime(actual_format)
    except (ValueError, TypeError):
        # Return original timestamp if conversion fails
        return str(timestamp)


@app.template_filter('format_time')
def format_time_filter(timestamp=None):
    """
    Format current or provided timestamp as HH:MM with AM/PM.
    
    Args:
        timestamp (int, optional): Unix timestamp. If None, uses current time.
    
    Returns:
        str: Formatted time string (e.g., "2:30 PM")
    """
    if timestamp is None:
        dt = datetime.now()
    else:
        dt = datetime.fromtimestamp(timestamp)
    return dt.strftime('%I:%M %p')


@app.template_filter('format_date_long')
def format_date_long_filter(timestamp=None):
    """
    Format current or provided timestamp as full date.
    
    Args:
        timestamp (int, optional): Unix timestamp. If None, uses current time.
    
    Returns:
        str: Formatted date string (e.g., "Saturday, January 11, 2026")
    """
    if timestamp is None:
        dt = datetime.now()
    else:
        dt = datetime.fromtimestamp(timestamp)
    return dt.strftime('%A, %B %d, %Y')


@app.template_filter('format_24h')
def format_24h_filter(timestamp=None):
    """
    Format current or provided timestamp in 24-hour format.
    
    Args:
        timestamp (int, optional): Unix timestamp. If None, uses current time.
    
    Returns:
        str: Formatted time string (e.g., "14:30")
    """
    if timestamp is None:
        dt = datetime.now()
    else:
        dt = datetime.fromtimestamp(timestamp)
    return dt.strftime('%H:%M')


@app.template_filter('time_ago')
def time_ago_filter(timestamp):
    """
    Calculate how long ago a timestamp was.
    
    Args:
        timestamp (int): Unix timestamp
    
    Returns:
        str: Human-readable time difference (e.g., "5 minutes ago")
    """
    dt = datetime.fromtimestamp(timestamp)
    now = datetime.now()
    diff = now - dt
    
    minutes = diff.total_seconds() / 60
    if minutes < 1:
        return "Just now"
    elif minutes < 60:
        return f"{int(minutes)} minute{'s' if int(minutes) != 1 else ''} ago"
    
    hours = minutes / 60
    if hours < 24:
        return f"{int(hours)} hour{'s' if int(hours) != 1 else ''} ago"
    
    days = hours / 24
    return f"{int(days)} day{'s' if int(days) != 1 else ''} ago"


@app.template_filter('sunrise_sunset')
def sunrise_sunset_filter(timestamp):
    """
    Format sunrise/sunset timestamp as readable time.
    
    Args:
        timestamp (int): Unix timestamp
    
    Returns:
        str: Formatted time (e.g., "6:45 AM")
    """
    if timestamp == 0:
        return "N/A"
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime('%I:%M %p')


@app.template_filter('location_time')
def location_time_filter(timestamp, timezone_offset=0):
    """
    Format timestamp as local time at the weather location.
    
    Args:
        timestamp (int): Unix timestamp
        timezone_offset (int): UTC offset in seconds (e.g., 3600 for UTC+1)
    
    Returns:
        str: Formatted time in location's timezone (e.g., "6:45 AM")
    """
    if timestamp == 0:
        return "N/A"
    # Create datetime from timestamp and adjust by timezone offset
    dt = datetime.utcfromtimestamp(timestamp) + timedelta(seconds=timezone_offset)
    return dt.strftime('%I:%M %p')


@app.template_filter('location_date_time')
def location_date_time_filter(timestamp, timezone_offset=0):
    """
    Format timestamp as date and time at the weather location.
    
    Args:
        timestamp (int): Unix timestamp
        timezone_offset (int): UTC offset in seconds
    
    Returns:
        str: Formatted date/time in location's timezone
    """
    if timestamp == 0:
        return "N/A"
    dt = datetime.utcfromtimestamp(timestamp) + timedelta(seconds=timezone_offset)
    return dt.strftime('%A, %B %d, %Y at %I:%M %p')


@app.template_filter('timezone_display')
def timezone_display_filter(timezone_code):
    """
    Convert timezone code to readable timezone name.
    
    Args:
        timezone_code (str): Timezone code (e.g., "GB", "US")
    
    Returns:
        str: Readable timezone display
    """
    timezone_map = {
        'GB': '🇬🇧 GMT/BST (UK)',
        'US': '🇺🇸 EST/CST/MST/PST (USA)',
        'CA': '🇨🇦 EST/CST/MST/PST (Canada)',
        'AU': '🇦🇺 AEST/ACST/AWST (Australia)',
        'IN': '🇮🇳 IST (India)',
        'JP': '🇯🇵 JST (Japan)',
        'FR': '🇫🇷 CET/CEST (France)',
        'DE': '🇩🇪 CET/CEST (Germany)',
        'NZ': '🇳🇿 NZST/NZDT (New Zealand)',
        'SG': '🇸🇬 SGT (Singapore)',
    }
    return timezone_map.get(timezone_code, f"Timezone: {timezone_code}")

# ============================================================================
# FLASK ROUTES
# ============================================================================

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Main route handler for the weather dashboard.
    
    Handles both GET requests (display the form) and POST requests 
    (fetch and display weather data).
    
    GET Request:
        - Displays the empty weather dashboard form
        
    POST Request:
        - Retrieves city, state, and country from form data
        - Calls get_weather_data() to fetch weather information
        - Renders the dashboard with weather data
    
    Form Parameters:
        - city (str): City name (required)
        - state (str): State/province code (optional)
        - country (str): Country code (optional)
    
    Returns:
        Rendered HTML template with weather data (if POST) or empty form (if GET)
    """
    # Get current timestamp for UI display
    current_time = datetime.now().timestamp()
    
    if request.method == "POST":
        # Extract form data from user input
        city_name = request.form["city"]
        state_name = request.form["state"]
        country_code = request.form["country"]
        
        # Fetch weather data from OpenWeatherMap API
        weather_data = get_weather_data(city_name, state_name, country_code)
        
        # Log the retrieved data (for debugging)
        print(weather_data)
        
        # Render template with weather data and current time
        return render_template("index.html", weather_data=weather_data, current_time=current_time)
    
    # GET request: show empty form with current time
    return render_template("index.html", current_time=current_time)

# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Start Flask development server
    # debug=True enables auto-reload and detailed error pages
    app.run(debug=True)