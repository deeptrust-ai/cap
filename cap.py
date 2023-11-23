from dataclasses import dataclass
from enum import Enum
import logging
import typing
import tweepy

import config

FORMAT = "%(asctime)s: %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)

EXPANSIONS = ["referenced_tweets.id", "attachments.media_keys"]
MEDIA_FIELDS = ["url", "duration_ms", "variants"]

CAP_HANDLE = "@capornot_"


class CapType(Enum):
    """Job Type of the cap checker"""

    DEEPFAKE = "deepfake"
    FACTCHECK = "factcheck"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


@dataclass
class ValidMention:
    mention: typing.Any
    parent_tweet: typing.Any
    cap_type: CapType


class CapClient:
    def __init__(self) -> None:
        self.client = get_client()
        self.api = get_api()
        self.me = self.client.get_me().data
        self.cache = []

    def tweet(self, text, **kwargs):
        return self.client.create_tweet(text=text, **kwargs)

    def get_tweet(self, id, **kwargs) -> tweepy.Response:
        return self.client.get_tweet(
            id=id, expansions=EXPANSIONS, media_fields=MEDIA_FIELDS, **kwargs
        )

    def get_mentions(self, **kwargs) -> typing.List[ValidMention]:
        mentions: typing.List[ValidMention] = []
        found_mentions = self._get_user_mentions(**kwargs).data

        if not found_mentions:
            logging.info("No mentions found.")
            return mentions

        logging.info(f"Found {len(found_mentions)} total mentions.")

        # check each Mention for a valid, referenced tweet
        for mention in found_mentions:
            if mention.referenced_tweets and mention.id not in self.cache:
                for ref_tweet in mention.referenced_tweets:
                    # referenced_tweets is an array, but is typially one item
                    if ref_tweet.type == "replied_to" or ref_tweet.type == "quoted":
                        tweet_response = self.get_tweet(ref_tweet.id)
                        cap_type = self._get_cap_type(mention.text)
                        if self._is_valid_parent_tweet(tweet_response) and cap_type:
                            valid: ValidMention = ValidMention(
                                mention=mention,
                                parent_tweet=tweet_response,
                                cap_type=cap_type,
                            )
                            mentions.append(valid)

        # add mention to cache
        self.cache += [m.mention.id for m in mentions]

        logging.info(f"Found {len(mentions)} valid mentions.")

        return mentions

    def _get_cap_type(self, tweet) -> typing.Optional[CapType]:
        """Checks if the text of the tweet is parsed correctly and has a cap job type."""
        # Check for CapType
        cap_command_line = tweet.split(" ")
        if cap_command_line[0].lower() != CAP_HANDLE.lower():
            return None

        cap_type = cap_command_line[1]

        if CapType.has_value(cap_type):
            return CapType(cap_type)

        return None

    def _is_valid_parent_tweet(self, tweet) -> bool:
        """Checks if tweet has a video"""
        # Check for media
        media = tweet.includes.get("media")

        if not media:
            return False

        return any([m.type == "video" for m in media])

    def _get_user_mentions(self, **kwargs) -> tweepy.Response:
        return self.client.get_users_mentions(
            id=self.me.id, expansions=EXPANSIONS, media_fields=MEDIA_FIELDS, **kwargs
        )


def get_client() -> tweepy.API:
    return tweepy.Client(
        config.bearer_token,
        consumer_key=config.api_key,
        consumer_secret=config.api_secret,
        access_token=config.access_token,
        access_token_secret=config.access_secret,
    )


def get_api():
    auth = tweepy.OAuth1UserHandler(
        config.api_key, config.api_secret, config.access_token, config.access_secret
    )

    api = tweepy.API(auth)

    return api
