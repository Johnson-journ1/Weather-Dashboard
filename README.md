
# 🌤️ Weather Dashboard

A beautiful and interactive weather dashboard application that provides real-time weather information and forecasts using the **OpenWeatherMap API**.

## 📋 Table of Contents

- [Features](#features)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [API Integration](#api-integration)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

### Current Weather Display
- **Real-time temperature** with "feels like" perception
- **Weather description** with weather condition icons
- **Location name** and geographic coordinates

### Key Weather Metrics
- **💨 Wind Speed** - Displayed in m/s and km/h
- **👁️ Visibility** - Shown in kilometers and meters
- **💧 Humidity** - Percentage of moisture in the air
- **📊 Pressure** - Atmospheric pressure in millibars

### Advanced Weather Information
- **☀️ UV Index** - Color-coded risk levels (Low, Moderate, High, Very High)
- **📊 24-Hour Forecast** - Hourly weather predictions with temperature and precipitation chance
- **📅 5-7 Day Forecast** - Daily predictions with high/low temperatures, humidity, and wind speed
- **⚠️ Weather Alerts** - Active weather warnings and alerts (when available)

### User Interface
- **Responsive Design** - Works seamlessly on desktop, tablet, and mobile devices
- **Beautiful Gradient Background** - Modern purple gradient theme
- **Interactive Cards** - Hover effects and smooth animations
- **Easy Search** - Simple location search with city, state, and country inputs

---

## 🖼️ Screenshots

The dashboard features:
- A prominent current weather display with large temperature and weather icon
- Four key metric cards showing wind speed, visibility, humidity, and pressure
- UV Index section with color-coded risk advisories
- 24-hour weather forecast with hourly predictions
- 5-7 day weather forecast with detailed daily information

---

## 🚀 Installation

### Prerequisites
- **Python 3.8+**
- **pip** (Python package manager)
- **OpenWeatherMap API Key** (free tier available)

### Step 1: Clone the Repository
```bash
git clone https://github.com/Johnson-journ1/Weather-Dashboard.git
cd Weather-Dashboard
```

### Step 2: Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

The main dependencies are:
- **Flask** - Web framework
- **requests** - HTTP library for API calls
- **python-dotenv** - Environment variable management

---

## ⚙️ Configuration

### Getting an OpenWeatherMap API Key

1. Visit [OpenWeatherMap](https://openweathermap.org/)
2. Sign up for a **free account**
3. Navigate to the API keys section
4. Copy your **API key**

### Setting Up Environment Variables

1. Create a `.env` file in the project root:
```bash
touch .env
```

2. Add your API key to the `.env` file:
```
API_KEY=your_api_key_here
```

3. The application will automatically load this key using `python-dotenv`

---

## 📖 Usage

### Starting the Application

```bash
# Make sure virtual environment is activated
python app.py
```

The application will start on `http://127.0.0.1:5000`

### Using the Dashboard

1. **Open the browser** and navigate to `http://localhost:5000`
2. **Enter a location**:
   - City name (e.g., "London")
   - State/Province code (optional, e.g., "10")
   - Country code (optional, e.g., "GB")
3. **Click "Get Weather"** to fetch weather data
4. **View the results**:
   - Current weather at the top
   - Key metrics in the cards
   - 24-hour forecast for hourly predictions
   - 5-7 day forecast for longer-term planning
   - UV index with health advisories

### Default Location
The dashboard comes pre-filled with "London, GB" as the default location for convenience.

---

## 📁 Project Structure

```
Weather-Dashboard/
├── app.py                          # Flask application entry point
├── weather.py                      # Weather data fetching logic
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables (API key)
├── README.md                      # This file
├── templates/
│   └── index.html                # Main dashboard UI
├── assets/
│   └── icons/                    # Weather icons
├── data/
│   └── weather_history.csv       # Historical weather data
├── tests/
│   ├── test_processing.py        # Weather data processing tests
│   └── test_forecast.py          # Forecast data tests
└── __pycache__/                  # Python cache files
```

### Key Files Description

#### `app.py` - Flask Application
- Main Flask application server
- Handles HTTP routes (GET and POST)
- Manages template rendering
- Contains custom Jinja2 filters for date formatting

#### `weather.py` - Weather API Integration
- `WeatherData` dataclass: Defines weather data structure
- `get_lat_lon()`: Fetches latitude/longitude from city name
- `get_current_weather()`: Retrieves current weather conditions
- `get_forecast_data()`: Fetches hourly and daily forecasts + UV index
- `main()`: Orchestrates all weather data collection

#### `templates/index.html` - User Interface
- Responsive HTML5 template
- Bootstrap 5 framework for styling
- Custom CSS for modern design
- Jinja2 templating for dynamic content
- JavaScript for client-side formatting

---

## 🔌 API Integration

### OpenWeatherMap API Endpoints Used

#### 1. **Current Weather API**
- **Endpoint**: `/data/2.5/weather`
- **Purpose**: Get current weather conditions
- **Data Retrieved**: Temperature, humidity, pressure, wind speed, visibility, weather description

#### 2. **5-Day Forecast API**
- **Endpoint**: `/data/2.5/forecast`
- **Purpose**: Get 5-day forecast with 3-hour intervals
- **Data Retrieved**: Hourly temperatures, precipitation chance, weather icons

#### 3. **UV Index API**
- **Endpoint**: `/data/2.5/uvi`
- **Purpose**: Get current UV index
- **Data Retrieved**: UV index value for sun protection recommendations

### Data Flow

```
User Input (City, State, Country)
           ↓
    get_lat_lon() → Fetch coordinates
           ↓
  get_current_weather() → Current conditions
           ↓
  get_forecast_data() → 24-hour & 7-day forecasts + UV index
           ↓
   WeatherData object created with all data
           ↓
   Rendered in HTML template
           ↓
   Beautiful dashboard displayed to user
```

---

## 🛠️ Technologies Used

### Backend
- **Python 3.8+** - Programming language
- **Flask** - Web framework
- **Requests** - HTTP requests library
- **python-dotenv** - Environment variable management

### Frontend
- **HTML5** - Markup language
- **CSS3** - Styling with gradients and animations
- **Bootstrap 5** - Responsive framework
- **JavaScript** - Client-side functionality
- **Jinja2** - Template engine

### APIs
- **OpenWeatherMap API** - Real-time weather data

### Development Tools
- **Git** - Version control
- **Virtual Environment** - Python package isolation

---

## 📊 Weather Data Reference

### UV Index Levels
| Range | Risk Level | Recommendation |
|-------|-----------|-----------------|
| 0-2 | Low | Wear sunscreen |
| 3-5 | Moderate | Use sunscreen |
| 6-7 | High | Extra protection needed |
| 8+ | Very High | Avoid sun exposure |

### Wind Speed Units
- **m/s** (meters per second) - Primary display
- **km/h** (kilometers per hour) - Conversion shown

### Visibility Units
- **km** (kilometers) - Primary display
- **m** (meters) - Detailed information

---

## 🧪 Testing

Run the test suite:

```bash
# Test weather data processing
python tests/test_processing.py

# Test forecast functionality
python tests/test_forecast.py
```

---

## 🤝 Contributing

We welcome contributions! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

---

## 📝 License

This project is open source and available under the MIT License.

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing issues for similar problems
- Provide detailed information about the problem

---

## 🌟 Future Enhancements

Planned features for future versions:
- [ ] Multiple location favorites/bookmarks
- [ ] Weather alerts email notifications
- [ ] Historical weather data analysis
- [ ] Weather maps integration
- [ ] Air quality index (AQI)
- [ ] Pollen count data
- [ ] Precipitation radar
- [ ] Dark mode theme
- [ ] Multi-language support

---

## 🔐 Security Notes

- Never commit your `.env` file to version control
- Keep your OpenWeatherMap API key private
- Use environment variables for sensitive data
- The API key should be stored in `.env` and added to `.gitignore`

---

**Last Updated**: January 2026

**Maintained by**: Johnson-journ1

Enjoy using the Weather Dashboard! 🌈☀️🌧️