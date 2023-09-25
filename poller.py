import logging

from modal import functions, Image, Stub, Secret

from cap import CapClient
from heatmap import create_heatmap, delete_heatmap

FORMAT = '%(asctime)s: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

class ScorelessException(Exception):
    pass


image = (
    Image.debian_slim(python_version="3.10")
    .pip_install_from_requirements("requirements.txt")
)
stub = Stub(
    "cap-poller",
    image=image,
    secrets=(
        Secret.from_dotenv(".env.prod"),
    ),
)

@stub.function()
async def poller(id: str, mention_tweet_id: int):
    logging.info("Capper poller starting...")
    cap = CapClient()

    logging.info(f"Getting results for job(id={id}, mention_tweet_id={mention_tweet_id})...")
    function_call = functions.FunctionCall.from_id(id)

    try:
        result = function_call.get(timeout=60 * 5)
    except TimeoutError as e:
        logging.error(f"Polling job(id={id}, mention_tweet_id={mention_tweet_id}) has timed out.")
        raise e
    
    # TODO: Add tweet
    logging.info(f"Job(id={id}, mention_tweet_id={mention_tweet_id}) completed with this result: {result}")
    scores = result.get("scores")
    segmented_predictions = result.get("segmented_predictions")
    if not scores:
        raise ScorelessException(f"Job(id={id}, mention_tweet_id={mention_tweet_id}) returned empty scores.")

    logging.info(f"Job(id={id}, mention_tweet_id={mention_tweet_id}) posting to twitter...") 
    media_ids = []
    for sg in segmented_predictions:
        create_heatmap(sg)
        media = cap.api.media_upload("heatmap.png")
        media_ids.append(media.media_id)
        delete_heatmap()

    
    cap.tweet(text=_tweet(scores[0]), in_reply_to_tweet_id=mention_tweet_id, media_ids=media_ids)


def _tweet(score: int):

    icon = "🟢"
    message = "DeepTrust Alpha did not detect generated speech. Yay! 🎉"
    percent = round(score * 100, 2)

    if 50 <= percent <= 85:
        icon = "🟡"
        message = "DeepTrust Alpha detects some traces that resemble generated speech. Tread carefully. 👀"
    elif percent > 85:
        icon = "🔴"
        message = "🚨 CAPPER ALERT 🚨\nDeepTrust Alpha is certain there is generated speech. We detect a capper. 🧢"


    tweet =  """Speech Analysis Complete!

============
Disclaimer: DeepTrust Speech is in early alpha. Research is still undergoing. Results may vary.
"""

    return tweet.format(icon=icon, percent=percent, message=message)