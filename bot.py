import tweepy
import os
from dotenv import load_dotenv
import requests
from urllib.request import urlretrieve
from pprint import PrettyPrinter
pp = PrettyPrinter()
from datetime import date
import schedule
import time
from fns import *
from fns import APODbot

'''
Sources:
https://stackoverflow.com/a/21595698/27063292 to figure out how to download
the file onto my device before I upload it to twitter.
https://docs.tweepy.org/en/stable/client.html tweepy documentation to figure
out how this works.

To implement:
I need to get date and use it as the date for the photo of the day.
I want a description. We can get the explanation but I don't know if it
fits on Twitter. Then I would have to create a reply my own post.
Once I can do that, then I need to make sure it runs everyday.
Python anywhere? I need the medium article for that. It was something about
making a twitter bot on medium

'''

#access twitter api
client, api = access_api()

# NASA key
API_KEY = "h4wYtdHjbgSaA1CwmCVAqRgCfs5PXaXrxnRdBBuZ"

bot = APODbot(client)

media_id = get_img()

#client.create_tweet(text="another cool photo", media_ids=[media_id])

text = get_text()

bot.job(text, media_id)
'''
schedule.every().day.at("12:00").do(bot.job, media_id)

while True:
    schedule.run_pending()
    time.sleep(1)
'''
