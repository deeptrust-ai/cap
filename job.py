from dotenv import load_dotenv

load_dotenv()

import os
import logging
import typing

from modal import functions, Image, Stub, Secret

from cap import CapClient

image = (
    Image.debian_slim(python_version="3.10")
    .pip_install_from_requirements("requirements.txt")
)
stub = Stub(
    "rawnet-predict-jobs",
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
    cap.tweet(text="Job completed")


