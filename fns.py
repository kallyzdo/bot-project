import os
import tweepy
import requests
from datetime import date
from dotenv import load_dotenv
from math import ceil

# NASA key
API_KEY = "h4wYtdHjbgSaA1CwmCVAqRgCfs5PXaXrxnRdBBuZ"
class APODbot:
    def __init__(self, client):
      self.client = client
      self.id = None

    def job(self, text, media):

        response = self.client.create_tweet(media_ids=[media])
        self.id = response.data["id"]

        # Figure out how this works
        amount_of_tweets = int(ceil(len(text) / 250 ))

        for _ in range(amount_of_tweets):
            self.client.create_tweet(text=(text[249*_:249*(_+1)].rsplit(' ', 1)[0]), in_reply_to_tweet_id=self.id)
            #print("", end="")
            self.client.create_tweet(str(text[249*_:249*(_+1)].rsplit(' ', 1)[1]) + str(text[249*(_+1):249*(_+1)].rsplit(' ', 1)[0]), in_reply_to_tweet_id=self.id)
        return 0 
    

def access_api():

    load_dotenv()
    # Getting the tokens.
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
    CONSUMER_KEY = os.getenv("CONSUMER_KEY")
    CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")

    # API v2
    client = tweepy.Client(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )

    # API v1.0
    auth = tweepy.OAuth1UserHandler(
        CONSUMER_KEY,
        CONSUMER_SECRET,
        ACCESS_TOKEN,
        ACCESS_TOKEN_SECRET
    )
    api = tweepy.API(auth)

    return client, api


#from some medium article I lost (find)
def fetchAPOD():
  URL_APOD = "https://api.nasa.gov/planetary/apod"
  today = str(date.today())
  params = {
      'api_key':API_KEY,
      'date':today,
      'hd':'True'
  }
  response = requests.get(URL_APOD,params=params).json()
  #pp.pprint(response["url"])
  photo = str(response["url"])

  return photo


def get_text():
  URL_APOD = "https://api.nasa.gov/planetary/apod"
  today = date.today()
  params = {
      'api_key':API_KEY,
      'date':today,
      'hd':'True'
  }
  response = requests.get(URL_APOD,params=params).json()
  text = response['explanation']
  return text

def get_img():

    client, api = access_api()
    image_url = fetchAPOD()
    # Content is returned as binary data,
    # written into a file that I created
    photo = requests.get(image_url).content
    with open("space.jpg", "wb") as file:
        file.write(photo)

    file_name = "space.jpg"
    media_path = os.path.abspath(file_name)
    print(media_path)
    media_id = api.media_upload(filename=media_path).media_id_string
    print(media_id)
   
    return media_id