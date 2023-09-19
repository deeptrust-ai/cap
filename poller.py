from dotenv import load_dotenv

load_dotenv()

import os
import logging
from typing import Any, List
from uuid import uuid1

from modal import gpu, Image, Mount, Secret, Stub, asgi_app


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

@stub.function(gpu="any", retries=3)
def poller():
    # add poller here
    pass