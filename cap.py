import tweepy

import config

class CapClient:
    def __init__(self) -> None:
        self.client = get_client()
        self.me = self.client.get_me().data

    def tweet(self, text, **args):
        return self.client.create_tweet(text=text, **args)
    
    def get_mentions(self, **args):
        return self.client.get_users_mentions(id=self.me.id, **args)

def get_client() -> tweepy.API:
    return tweepy.Client(config.bearer_token,  consumer_key=config.api_key, consumer_secret=config.api_secret, access_token=config.access_token, access_token_secret=config.access_secret)

def get_api():
    auth = tweepy.OAuthHandler(config.api_key, config.api_key)
    auth.set_access_token(config.access_token, config.access_secret)

    api = tweepy.API(auth)
    
    return api