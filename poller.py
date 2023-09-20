import logging

from modal import functions, Image, Stub, Secret

from cap import CapClient

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
async def poller(id: str):
    logging.info("Capper poller starting...")
    cap = CapClient()

    print(f"Getting results for job(id={id})...")
    function_call = functions.FunctionCall.from_id(id)

    try:
        result = function_call.get(timeout=60 * 5)
    except TimeoutError as e:
        logging.error(f"Polling job (id={id}) has timed out.")
        raise e
    
    # TODO: Add tweet
    print(f"Job (id={id}) completed with this result: {result}")
    scores = result.get("scores")
    if not scores:
        raise ScorelessException(f"Job (id={id}) returned empty scores.")
        
    cap.tweet(text=f"Job completed -- {','.join([score for score in scores])}")