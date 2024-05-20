import requests, os, sys, logging
from datetime import datetime

URL = "https://api.weatherapi.com/v1/"

logger = logging.getLogger(__name__)
logging.basicConfig(filename="errors.log", encoding="utf-8", level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

with open(".key.txt") as file:
    KEY = file.read()

def getCurrentTemp(KEY=KEY, URL=URL):

    # Altering url to get current data
    URL += ("current.json")

    city = "Wroclaw"

    # Call API
    response = requests.get(URL, params={"key": KEY, "q": city})

    if response:
        # Extract relevant data from JSON object
        temp = response.json()["current"]["temp_c"]

        print(f"It's currently {temp} C degrees in {city}")
    else:
        logger.error("There was an error processing request for Wroclaw weather")

if __name__ == "__main__":
    getCurrentTemp()