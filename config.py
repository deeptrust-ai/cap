from dotenv import load_dotenv
load_dotenv()

import os

api_key = os.environ.get("TWITTER_API_KEY")
api_secret = os.environ.get("TWITTER_API_SECRET")

bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")

access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
access_secret = os.environ.get("TWITTER_ACCESS_SECRET")