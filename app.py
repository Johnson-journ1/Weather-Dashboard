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
from datetime import datetime

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
    if request.method == "POST":
        # Extract form data from user input
        city_name = request.form["city"]
        state_name = request.form["state"]
        country_code = request.form["country"]
        
        # Fetch weather data from OpenWeatherMap API
        weather_data = get_weather_data(city_name, state_name, country_code)
        
        # Log the retrieved data (for debugging)
        print(weather_data)
        
        # Render template with weather data
        return render_template("index.html", weather_data=weather_data)
    
    # GET request: show empty form
    return render_template("index.html")

# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Start Flask development server
    # debug=True enables auto-reload and detailed error pages
    app.run(debug=True)