from __future__ import annotations

import logging
import random
from langchain_core.tools import tool

logger = logging.getLogger(__name__)

# Mock weather conditions pool
WEATHER_CONDITIONS = [
    "Sunny",
    "Partly Cloudy",
    "Cloudy",
    "Rainy",
    "Thunderstorm",
    "Foggy",
    "Snowy",
    "Clear",
    "Drizzle",
    "Overcast"
]


@tool("get_weather")
def get_weather_tool(location: str) -> str:
    """Get current weather information for a location.

    Args:
        location: The city name or location to get weather for (e.g., "London", "New York", "Tokyo").
    """
    logger.info(f"> Fetching weather for location: {location}")
    
    # Generate randomized mock weather data
    temp_c = random.randint(-10, 35)
    temp_f = int(temp_c * 9/5 + 32)
    condition = random.choice(WEATHER_CONDITIONS)
    humidity = random.randint(30, 95)
    wind_speed = random.randint(0, 50)
    
    weather_info = (
        f"Weather in {location}:\n"
        f"Temperature: {temp_c}°C ({temp_f}°F)\n"
        f"Condition: {condition}\n"
        f"Humidity: {humidity}%\n"
        f"Wind: {wind_speed} km/h"
    )

    logger.info(f"> Weather data: {weather_info}")
    
    return weather_info
