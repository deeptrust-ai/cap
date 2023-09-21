from datetime import datetime
import logging
import time

from modal import Function
from tweepy.errors import TooManyRequests

from cap import CapClient, ValidMention

FORMAT = '%(asctime)s: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

cap = CapClient()
logging.info("Capper Checker starting...")

def launch_job(mention: ValidMention) -> None:
    # will launch a modal job to fact check tweet (API request)
    logging.info(f"Launching twitter predict job for mention(id={mention.mention.id})...")
    twitter_predict = Function.lookup("rawnet-predict-jobs", "twitter_predict")
    parent_tweet = mention.parent_tweet.data
    predict_job = twitter_predict.spawn(parent_tweet.id, "ss")
    job_id = predict_job.object_id

    # launch a poller job to update with tweet (modal function launch)
    logging.info("Launching poller...")
    poller = Function.lookup("cap-poller", "poller")
    poller.spawn(job_id)


start_time = datetime.now()
while True:
    # Get the mentions for your bot's user ID.
    logging.info(f"Getting mentions starting from time ({start_time})")

    try:
        mentions = cap.get_mentions(start_time=start_time)
    except TooManyRequests:
        sleep_time = 60 * 5 # five minutes
        logging.error(f"TooManyRequests thrown. Sleeping for {sleep_time}s.")

        time.sleep(sleep_time)
        continue
    
    logging.info(f"Found {len(mentions)} valid mentions. Launching jobs...")
    
    for mention in mentions:
        # TODO: Test launch job
        launch_job(mention)
    
    # update start time
    start_time = datetime.now()

    # sleep
    logging.info("sleep...")
    time.sleep(30)

    
