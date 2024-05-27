import tweepy
import logging
import logging.handlers
import os
import tempfile
from keys import *
from pogoda import getCurrentTemp

# Configure tweepy and authenticate the API
client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# Logger configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set the default logging level to DEBUG

# File handler for logging to a file with rotation
file_handler = logging.handlers.RotatingFileHandler(
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

def tweet(text="test"):
    """
    Post a tweet with the given text.
    
    Args:
    text (str): The text content of the tweet.
    """
    try:
        response = client.create_tweet(text=text)
        tweet_id = response.data["id"]
        write_tweet_id_to_file(tweet_id)
        logger.info(f"Tweet posted successfully: {tweet_id}")
    except Exception as e:
        logger.warning(f"Error while posting the tweet: {e}")

def write_tweet_id_to_file(tweet_id):
    """
    Write the tweet ID to the file atomically.
    
    Args:
    tweet_id (int): The ID of the tweet to be written to the file.
    """
    try:
        with tempfile.NamedTemporaryFile('w', delete=False, dir='.') as temp_file:
            temp_file.write(f"{tweet_id}\n")
        os.replace(temp_file.name, "tweety.txt")
        logger.info(f"Tweet ID {tweet_id} written to file successfully.")
    except Exception as e:
        logger.error(f"Error writing tweet ID to file: {e}")

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
        if os.path.exists("tweety.txt"):
            with open("tweety.txt", "r") as myfile:
                tweet_ids = myfile.read().strip().split("\n")
                if tweet_ids:
                    return int(tweet_ids[-1].strip())
        logger.info("No tweet IDs found in the file.")
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