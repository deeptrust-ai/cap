from datetime import datetime
import logging
import time

from cap import CapClient

FORMAT = '%(asctime)s: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

cap = CapClient()
logging.info("Capper Checker starting...")

start_time = datetime.now()
while True:
    # Get the mentions for your bot's user ID.
    logging.info(f"Getting mentions starting from time ({start_time})")
    mentions = cap.get_mentions()

    # Iterate over the results and check if each mention is a reply to a tweet with a video.
    if mentions.data:
        for mention in mentions.data:

            if mention.in_reply_to_user_id is not None:
                logging.info(f"Mention found: {mention}")

                # The mention is a reply to a tweet.
                tweet = cap.client.get_tweet(id=mention.in_reply_to_user_id)

                # Check if the tweet contains a video.
                if tweet.data.entities.get("media", []):
                    for medium in tweet.data.entities["media"]:
                        if medium.type == "video":
                            # The mention is a reply to a tweet with a video.
                            # Do something with the mention.
                            logging.info(f"Tweet candidate found: (id={tweet.data.id}, text={tweet.data.text})")
    
    # update start time
    start_time = datetime.now()

    # sleep
    logging.info("sleep...")
    time.sleep(30)

    
