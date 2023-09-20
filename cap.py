import tweepy

import config

EXPANSIONS = ["referenced_tweets.id", "attachments.media_keys"]
MEDIA_FIELDS = ["url", "duration_ms", "variants"]

class CapClient:
    def __init__(self) -> None:
        self.client = get_client()
        self.me = self.client.get_me().data

    def tweet(self, text, **args):
        return self.client.create_tweet(text=text, **args)
    
    def get_tweet(self, id, **args):
        return self.client.get_tweet(id=id, expansions=EXPANSIONS, media_fields=MEDIA_FIELDS, **args)

    def get_mentions(self, **args):
        mentions = []
        found_mentions = self._get_user_mentions(**args).data

        if not found_mentions: return mentions

        for mention in found_mentions:
            if mention.referenced_tweets:
                for rtweet in mention.referenced_tweets:
                    if self._is_valid_tweet(rtweet):
                        tweet = self.get_tweet(rtweet.id)
                        mentions.append(dict(mention=mention, parent_tweet=tweet))

        return mentions

    def _is_valid_tweet(self, tweet):
        return tweet.type == 'replied_to'
    
    def _get_user_mentions(self, **args):
        return self.client.get_users_mentions(id=self.me.id, expansions=EXPANSIONS, media_fields=MEDIA_FIELDS, **args)



def get_client() -> tweepy.API:
    return tweepy.Client(config.bearer_token,  consumer_key=config.api_key, consumer_secret=config.api_secret, access_token=config.access_token, access_token_secret=config.access_secret)

def get_api():
    auth = tweepy.OAuthHandler(config.api_key, config.api_key)
    auth.set_access_token(config.access_token, config.access_secret)

    api = tweepy.API(auth)
    
    return api