"""DeepTrust API"""
# TODO: Create DT Client
from dotenv import load_dotenv
load_dotenv()

import os
import requests

api_url = os.environ.get("API_URL")

if api_url == None:
    print("Warning: DeepTrust API not found")

def health_check():
    return requests.get(api_url).json()

def twitter_transcribe(tweet_url: str):
    request_url = api_url + "/transcribe/twitter"
    params = dict(url=tweet_url)

    result = requests.get(request_url, params=params).json()

    return result

if __name__ == "__main__":
    # print(health_check())
    print(twitter_transcribe("https://twitter.com/amanmibra/status/1727051006054420532"))