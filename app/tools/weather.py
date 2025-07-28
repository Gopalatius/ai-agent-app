import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenWeatherMap API key from environment variables
# IMPORTANT: Replace "YOUR_OPENWEATHER_API_KEY" with your actual key
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "YOUR_OPENWEATHER_API_KEY")
OPENWEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(location: str = "Chicago") -> str:
    """
    Fetches current weather information for a given location using OpenWeatherMap API.

    Args:
        location (str): The city name or location to get weather for.

    Returns:
        str: A human-readable string describing the weather, or an error message.
    """
    if not OPENWEATHER_API_KEY or OPENWEATHER_API_KEY == "YOUR_OPENWEATHER_API_KEY":
        return "Weather API key not configured. Please set OPENWEATHER_API_KEY in your environment."

    params = {
        "q": location,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric" # For Celsius temperature
    }
    try:
        response = requests.get(OPENWEATHER_BASE_URL, params=params)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        if data.get("cod") == 200:
            # Extract relevant weather information
            main_data = data.get("main", {})
            weather_description = data.get("weather", [{}])[0].get("description", "unknown")
            temperature = main_data.get("temp")
            city_name = data.get("name")
            country = data.get("sys", {}).get("country")

            if temperature is not None:
                return f"It's {temperature}°C and {weather_description} in {city_name}, {country}."
            else:
                return f"Weather data available for {city_name}, {country}, but temperature is missing."
        else:
            # Handle API-specific errors (e.g., city not found)
            return f"Could not retrieve weather for {location}: {data.get('message', 'Unknown error from API')}"
    except requests.exceptions.RequestException as e:
        # Handle network-related errors (e.g., connection refused, DNS error)
        return f"Error fetching weather for {location}: A network error occurred: {e}"
    except Exception as e:
        # Catch any other unexpected errors
        return f"An unexpected error occurred while processing weather data: {e}"