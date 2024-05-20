import tweepy, logging
from keys import *

# Konfiguracja tweepy oraz autoryzacja API
client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# Inicjacja loggera
logger = logging.getLogger(__name__)
logging.basicConfig(filename="errors.log", encoding="utf-8", level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def tweet():
    try:
        client.create_weet(text = "Hello")
    except:
        logger.warning("There was an error while posting the tweet")

tweet()