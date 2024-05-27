import tweepy
import logging
import os
from keys import *
from pogoda import getCurrentTemp

# Configure tweepy and authenticate the API
client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# Initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="errors.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p'
)

def tweet(text="test"):
    """
    Post a tweet with the given text.
    
    Args:
    text (str): The text content of the tweet.
    """
    try:
        response = client.create_tweet(text=text)
        tweet_id = response.data["id"]
        with open("tweety.txt", "a") as myfile:
            myfile.write(f"{tweet_id}\n")
        logger.info(f"Tweet posted successfully: {tweet_id}")
    except Exception as e:
        logger.warning(f"Error while posting the tweet: {e}")

def remove(tweet_id):
    """
    Remove a tweet with the given ID.
    
    Args:
    tweet_id (int): The ID of the tweet to be removed.
    """
    try:
        client.delete_tweet(id=tweet_id)
        logger.info(f"Tweet deleted successfully: {tweet_id}")
    except Exception as e:
        logger.error(f"Error while deleting the tweet: {e}")

def read_last_tweet_id():
    """
    Read the ID of the last tweet from the file.
    
    Returns:
    int: The ID of the last tweet.
    """
    try:
        with open("tweety.txt", "r") as myfile:
            tweet_ids = myfile.read().strip().split("\n")
            if tweet_ids:
                return int(tweet_ids[-1].strip())
    except Exception as e:
        logger.error(f"Error reading last tweet ID: {e}")
    return None

if __name__ == "__main__":
    # Example usage
    try:
        tweet(getCurrentTemp())  # Post a tweet with the current temperature
        tweet("Another test tweet")  # Post a generic test tweet
        last_tweet_id = read_last_tweet_id()
        if last_tweet_id:
            remove(last_tweet_id)  # Remove the last tweeted tweet
        else:
            logger.info("No tweet found to delete.")
    except Exception as e:
        logger.error(f"An error occurred in the main execution block: {e}")