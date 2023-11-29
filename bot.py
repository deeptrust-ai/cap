from datetime import datetime
import logging
import time
import os

from modal import Function
from tweepy.errors import TooManyRequests
import pytz

from cap import CapClient, CapType, ValidMention

FORMAT = "%(asctime)s: %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)

SLEEP_TIME = int(os.environ.get("SLEEP_TIME", "30"))

cap = CapClient()
logging.info("Capper Checker starting...")


def launch_deepfake_job(mention: ValidMention) -> None:
    # will launch a modal job to fact check tweet (API request)
    # TODO: Use api to launch tweet job
    logging.info(
        f"Launching twitter predict job for mention(id={mention.mention.id})..."
    )
    twitter_predict = Function.lookup("rawnet-predict-jobs", "twitter_predict")
    mention_tweet = mention.mention
    parent_tweet = mention.parent_tweet.data
    predict_job = twitter_predict.spawn(parent_tweet.id, "ss")
    job_id = predict_job.object_id

    # launch a poller job to update with tweet (modal function launch)
    logging.info(f"Launching poller(job_id={job_id})...")
    poller = Function.lookup("cap-poller", "poller")
    poller.spawn(job_id, mention_tweet.id)


start_time = datetime.now(tz=pytz.utc)
while True:
    # Get the mentions for your bot's user ID.
    logging.info(f"Getting mentions starting from time ({start_time})")

    try:
        mentions = cap.get_mentions(start_time=start_time)
    except TooManyRequests:
        sleep_time = SLEEP_TIME * 5
        logging.error(f"TooManyRequests thrown. Sleeping for {sleep_time}s.")

        time.sleep(sleep_time)
        continue

    for mention in mentions:
        if mention.cap_type == CapType.DEEPFAKE:
            print(
                f"Starting deepfake job for mention(tweet_id={mention.mention.id})..."
            )
            launch_deepfake_job(mention)
        elif mention.cap_type == CapType.FACTCHECK:
            print(
                f"Starting factcheck job for mention(tweet_id={mention.mention.id})..."
            )
            # TODO: Add factcheck job

    # update start time
    start_time = datetime.now(tz=pytz.utc)

    # sleep
    logging.info(f"Sleeping for {SLEEP_TIME}s...")
    time.sleep(SLEEP_TIME)
