#!/usr/bin/env python

import tweepy
from config import api_key, api_secret, client_id, client_secret

# From your app settings page
CONSUMER_KEY = api_key
CONSUMER_SECRET = api_secret

auth = tweepy.OAuth2UserHandler(
    client_id=client_id,
    redirect_uri="https://localhost:3000/",
    scope=['tweet.read', 'tweet.write', 'offline.access', 'users.read'],
    client_secret=client_secret
)
auth_url = auth.get_authorization_url()

print ('Please authorize: ' + auth_url)

verifier = input('Paste returned URL: ').strip()

access_token = auth.fetch_token(verifier)

print ("ACCESS_KEY = ", access_token)
# print ("ACCESS_SECRET = " +  auth.access_token_secret)