from dotenv import load_dotenv
load_dotenv()

import os

api_key = os.environ.get("TWITTER_API_KEY")
api_secret = os.environ.get("TWITTER_API_SECRET")

bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

cap_token = os.environ.get("CAP_ACCESS_TOKEN")