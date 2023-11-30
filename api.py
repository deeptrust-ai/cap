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

    return result.get('output')

def verity(text: str):
    request_url = api_url + "/verity/text"
    body = dict(transcription=text)

    result = requests.post(request_url, json=body).json()

    return result.get('output')

if __name__ == "__main__":
    # print(health_check())
    example_tweet = "https://twitter.com/amanmibra/status/1727051006054420532"

    print("Transcribing...")
    transcription = twitter_transcribe(example_tweet)
    print(f"Transcription Result: {transcription}\n----------")
    print("Fact checking...")
    fact_check = verity(transcription)

    print(f'Fact Check Output: {fact_check}')
