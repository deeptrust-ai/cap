import tweepy

from config import cap_token

class CapClient:
    def __init__(self) -> None:
        self.client = tweepy.Client(cap_token)
        self.me = self.client.get_me(user_auth=False).data

    def tweet(self, text, **args):
        return self.client.create_tweet(text=text, user_auth=False, **args)
    
    def get_mentions(self, **args):
        return self.client.get_users_mentions(id=self.me.id, **args)

def get_client():
    return tweepy.Client(cap_token)