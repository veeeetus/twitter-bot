import tweepy, logging
from keys import *
from pogoda import getCurrentTemp

# Konfiguracja tweepy oraz autoryzacja API
client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# Inicjacja loggera
logger = logging.getLogger(__name__)
logging.basicConfig(filename="errors.log", encoding="utf-8", level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def tweet():
    try:
        temp = client.create_tweet(text = "test2")
        with open("tweety.txt", "a") as myfile:
            myfile.write(temp.data["id"])
    except:
        logger.warning("There was an error while posting the tweet")

def remove():
    while True:
            try:
                post_id = int(input("Please provide the ID of the post you want to delete: "))
                client.delete_tweet(id = post_id)
                print("post deleted successfully")
                return
            except:
                with open("tweety.txt", "r") as myfile:
                    lista_id = myfile.read()
                print("You provided the wrong ID. List of IDs: ",lista_id)
if __name__ == "__main__":
    remove()