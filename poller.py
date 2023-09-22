import logging

from modal import functions, Image, Stub, Secret

from cap import CapClient

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
        Secret.from_dotenv(),
    ),
)

@stub.function()
async def poller(id: str, parent_tweet_id):
    logging.info("Capper poller starting...")
    cap = CapClient()

    logging.info(f"Getting results for job(id={id}, parent_tweet_id={parent_tweet_id})...")
    function_call = functions.FunctionCall.from_id(id)

    try:
        result = function_call.get(timeout=60 * 5)
    except TimeoutError as e:
        logging.error(f"Polling job(id={id}, parent_tweet_id={parent_tweet_id}) has timed out.")
        raise e
    
    # TODO: Add tweet
    logging.info(f"Job(id={id}, parent_tweet_id={parent_tweet_id}) completed with this result: {result}")
    scores = result.get("scores")
    if not scores:
        raise ScorelessException(f"Job(id={id}, parent_tweet_id={parent_tweet_id}) returned empty scores.")

    logging.info(f"Job(id={id}, parent_tweet_id={parent_tweet_id}) posting to twitter...")    
    cap.tweet(text=f"Job completed -- {','.join(map(str, scores))}", in_reply_to_tweet_id=parent_tweet_id)