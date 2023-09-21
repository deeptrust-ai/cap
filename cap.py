from dataclasses import dataclass
import typing
import tweepy

import config

EXPANSIONS = ["referenced_tweets.id", "attachments.media_keys"]
MEDIA_FIELDS = ["url", "duration_ms", "variants"]

# TODO: Rename ValidMention
@dataclass
class ValidMention:
    mention: typing.Any
    parent_tweet: typing.Any

class CapClient:
    def __init__(self) -> None:
        self.client = get_client()
        self.me = self.client.get_me().data

    def tweet(self, text, **kwargs):
        return self.client.create_tweet(text=text, **kwargs)
    
    def get_tweet(self, id, **kwargs) -> tweepy.Response:
        return self.client.get_tweet(id=id, expansions=EXPANSIONS, media_fields=MEDIA_FIELDS, **kwargs)

    def get_mentions(self, **kwargs) -> typing.List[ValidMention]:
        mentions: typing.List[ValidMention] = []
        found_mentions = self._get_user_mentions(**kwargs).data

        if not found_mentions: return mentions

        # check each Mention for a valid, referenced tweet
        for mention in found_mentions:
            if mention.referenced_tweets:
                for ref_tweet in mention.referenced_tweets:
                    # referenced_tweets is an array, but is typially one item
                    if ref_tweet.type == 'replied_to':
                        tweet_response = self.get_tweet(ref_tweet.id)
                        if self._is_valid_tweet(tweet_response):
                            valid: ValidMention = ValidMention(mention=mention, parent_tweet=tweet_response)
                            mentions.append(valid)

        return mentions

    def _is_valid_tweet(self, tweet) -> bool:
        media = tweet.includes.get("media")

        if not media: return False

        return any([m.type == "video" for m in media])
    
    def _get_user_mentions(self, **kwargs) -> tweepy.Response:
        return self.client.get_users_mentions(id=self.me.id, expansions=EXPANSIONS, media_fields=MEDIA_FIELDS, **kwargs)



def get_client() -> tweepy.API:
    return tweepy.Client(config.bearer_token,  consumer_key=config.api_key, consumer_secret=config.api_secret, access_token=config.access_token, access_token_secret=config.access_secret)

def get_api():
    auth = tweepy.OAuthHandler(config.api_key, config.api_key)
    auth.set_access_token(config.access_token, config.access_secret)

    api = tweepy.API(auth)
    
    return api