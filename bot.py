from datetime import datetime
import logging
import time

from cap import CapClient, ValidMention

FORMAT = '%(asctime)s: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

cap = CapClient()
logging.info("Capper Checker starting...")

def launch_job(mention: ValidMention) -> None:
    # will launch a modal job to fact check tweet (API request)
    # will launch a poller job to update with tweet (modal function launch)
    pass

start_time = datetime.now()
while True:
    # Get the mentions for your bot's user ID.
    logging.info(f"Getting mentions starting from time ({start_time})")
    mentions = cap.get_mentions(
        start_time=start_time
    )
    
    for mention in mentions:
        launch_job(mention)
    
    # update start time
    start_time = datetime.now()

    # sleep
    logging.info("sleep...")
    time.sleep(30)

    
