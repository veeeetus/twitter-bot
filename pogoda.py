# weather.py
import requests
import os
import logging
from logging.handlers import RotatingFileHandler

# Base URL for the Weather API
BASE_URL = os.getenv("WEATHER_API_URL", "https://api.weatherapi.com/v1/")

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# File handler for logging to a file with rotation
file_handler = RotatingFileHandler(
    filename="errors.log",
    maxBytes=1024 * 1024 * 5,  # 5 MB
    backupCount=5,
    encoding="utf-8"
)
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p'
)
file_handler.setFormatter(file_formatter)

# Stream handler for logging to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Read API key from the file
try:
    with open(".key.txt") as file:
        API_KEY = file.read().strip()
except FileNotFoundError:
    logger.error("API key file not found. Please make sure .key.txt is present.")
    raise
except Exception as e:
    logger.error(f"Error reading API key: {e}")
    raise

def get_current_temp(api_key=API_KEY, base_url=BASE_URL, city="Wroclaw"):
    """
    Fetch the current temperature for a given city.

    Args:
    api_key (str): API key for authentication.
    base_url (str): Base URL for the weather API.
    city (str): The city to get the weather for.

    Returns:
    str: A string with the current temperature.
    """
    url = f"{base_url}current.json"

    try:
        response = requests.get(url, params={"key": api_key, "q": city})
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        
        data = response.json()
        temp = data["current"]["temp_c"]
        return f"It's currently {temp} C degrees in {city}"

    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {e}")
    except KeyError as e:
        logger.error(f"Key error: {e} - Response data: {response.text}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

    return "There was an error retrieving the weather data."