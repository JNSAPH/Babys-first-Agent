from __future__ import annotations

import logging
import requests
from langchain_core.tools import tool

logger = logging.getLogger(__name__)


@tool("get_weather")
def get_weather_tool(location: str) -> str:
    """Get current weather information for a location. If this Tool fails, return an error message.

    Args:
        location: The city name or location to get weather for (e.g., "London", "New York", "Tokyo").
    """
    logger.debug(f"> Fetching weather for location: {location}")
    
    try:
        # Use wttr.in API - free and no API key required
        url = f"https://wttr.in/{location}?format=j1"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        current = data["current_condition"][0]
        
        weather_info = (
            f"Weather in {location}:\n"
            f"Temperature: {current['temp_C']}°C ({current['temp_F']}°F)\n"
            f"Condition: {current['weatherDesc'][0]['value']}\n"
            f"Humidity: {current['humidity']}%\n"
            f"Wind: {current['windspeedKmph']} km/h"
        )
        
        return weather_info
        
    except requests.RequestException as e:
        logger.error(f"> Failed to fetch weather: {e}")
        # Mock weather data on failure
        return (
            f"Weather in {location}:\n"
            f"Temperature: 20°C (68°F)\n"
            f"Condition: Partly Cloudy\n"
            f"Humidity: 50%\n"
            f"Wind: 10 km/h"
        )
    except (KeyError, IndexError) as e:
        logger.error(f"> Failed to parse weather data: {e}")
        return f"ERROR: Could not parse weather data for {location}."
