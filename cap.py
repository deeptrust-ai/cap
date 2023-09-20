import tweepy

import config

class CapClient:
    def __init__(self) -> None:
        self.client = get_client()
        self.me = self.client.get_me().data

    def tweet(self, text, **args):
        return self.client.create_tweet(text=text, **args)
    
    def get_mentions(self, **args):
        mentions = []
        found_mentions = self.client.get_users_mentions(id=self.me.id, expansions=["referenced_tweets.id"], **args).data

        if found_mentions:
            # print(f"found: {found_mentions}")
            for mention in found_mentions:
                print(f"men: {mention}")
                if mention.referenced_tweets:
                    mentions.append([mention for tweet in mention.referenced_tweets if self._is_valid_tweet(tweet)])

        return mentions

    def _is_valid_tweet(self, tweet):
        return tweet.type == 'replied_to'



def get_client() -> tweepy.API:
    return tweepy.Client(config.bearer_token,  consumer_key=config.api_key, consumer_secret=config.api_secret, access_token=config.access_token, access_token_secret=config.access_secret)

def get_api():
    auth = tweepy.OAuthHandler(config.api_key, config.api_key)
    auth.set_access_token(config.access_token, config.access_secret)

    api = tweepy.API(auth)
    
    return api