"""
Beginner-friendly API integration example
Uses Open-Meteo (https://open-meteo.com/) — free, no API key needed!

Install required library:
    pip install requests

Run:
    python weather_api.py
"""

import requests  # For making HTTP requests


# ─────────────────────────────────────────────
# STEP 1: Define the API endpoint and parameters
# ─────────────────────────────────────────────

BASE_URL = "https://api.open-meteo.com/v1/forecast"

# Coordinates for New York City
params = {
    "latitude": 40.7128,
    "longitude": -74.0060,
    "current": "temperature_2m,wind_speed_10m,relative_humidity_2m,weather_code",
    "hourly": "temperature_2m,precipitation_probability",
    "temperature_unit": "fahrenheit",
    "wind_speed_unit": "mph",
    "timezone": "America/New_York",
    "forecast_days": 1,
}


# ─────────────────────────────────────────────
# STEP 2: Make the API call
# ─────────────────────────────────────────────

def get_weather(latitude: float, longitude: float) -> dict:
    """
    Fetches current weather data for the given coordinates.

    Args:
        latitude:  Latitude of the location
        longitude: Longitude of the location

    Returns:
        A dictionary containing the weather data (parsed JSON)

    Raises:
        requests.HTTPError: If the server returns an error status code
    """
    # Update params with the provided coordinates
    params["latitude"] = latitude
    params["longitude"] = longitude

    print(f"Fetching weather for ({latitude}, {longitude})...")

    # Send the GET request
    response = requests.get(BASE_URL, params=params, timeout=10)

    # Raise an error if the request failed (e.g. 404, 500)
    response.raise_for_status()

    # Parse the JSON body into a Python dictionary
    data = response.json()

    return data


# ─────────────────────────────────────────────
# STEP 3: Parse and display the response
# ─────────────────────────────────────────────

# Map weather codes to human-readable descriptions
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Icy fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    80: "Slight showers", 81: "Moderate showers", 82: "Violent showers",
    95: "Thunderstorm", 96: "Thunderstorm with hail",
}

def display_weather(data: dict) -> None:
    """Prints a neatly formatted weather summary."""

    current = data["current"]
    hourly  = data["hourly"]

    # Pull out the values we want
    temp       = current["temperature_2m"]
    wind       = current["wind_speed_10m"]
    humidity   = current["relative_humidity_2m"]
    code       = current["weather_code"]
    condition  = WEATHER_CODES.get(code, "Unknown")
    timezone   = data["timezone"]

    print("\n" + "=" * 40)
    print(f"  Current weather  |  {timezone}")
    print("=" * 40)
    print(f"  Condition  : {condition}")
    print(f"  Temperature: {temp} °F")
    print(f"  Wind speed : {wind} mph")
    print(f"  Humidity   : {humidity} %")
    print("=" * 40)

    # Show the next 6 hours of forecast
    print("\n  Next 6 hours:")
    times  = hourly["time"][:6]
    temps  = hourly["temperature_2m"][:6]
    precip = hourly["precipitation_probability"][:6]

    for t, temp_h, rain in zip(times, temps, precip):
        hour = t.split("T")[1]  # Extract "HH:MM" from "2024-01-01T08:00"
        print(f"    {hour}  →  {temp_h:5.1f} °F   Rain chance: {rain}%")

    print()


# ─────────────────────────────────────────────
# STEP 4: Handle errors gracefully
# ─────────────────────────────────────────────

def main():
    # You can change these coordinates to any city!
    # New York:   40.7128, -74.0060
    # London:     51.5074,  -0.1278
    # Tokyo:      35.6762, 139.6503
    # Sydney:    -33.8688, 151.2093
    LATITUDE  = 40.7128
    LONGITUDE = -74.0060

    try:
        weather_data = get_weather(LATITUDE, LONGITUDE)
        display_weather(weather_data)

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect. Check your internet connection.")

    except requests.exceptions.Timeout:
        print("Error: The request timed out. Try again later.")

    except requests.exceptions.HTTPError as e:
        print(f"Error: Server returned an error — {e}")

    except KeyError as e:
        print(f"Error: Unexpected response format — missing key {e}")


if __name__ == "__main__":
    main()