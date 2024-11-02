import os
import json
from base64 import b64encode
from construct.core import Int
import requests
from dotenv import load_dotenv
import string
import random
from pydantic import BaseModel

from solders import instruction

load_dotenv()
BRIDGE_KEY = os.environ.get("BRIDGE_KEY")
BRIDGE_CUSTOMER = os.environ.get("BRIDGE_CUSTOMER_ID")

class Bridge(BaseModel):
    amount: float
    id: str
    id_key: str
    to_address: str
    from_address: str


def create_bridge(amount: str, from_address: str, to_address: str, id_key: str | None):
    headers = {
      'Content-Type': 'application/json',
      'Api-Key': BRIDGE_KEY,
    }
    url = "https://api.bridge.xyz/v0/transfers"

    # Generate random key
    headers["Idempotency-Key"] = id_key or _get_random_string()
    # print(headers["Idempotency-Key"])

    data = json.dumps({
        "amount": amount,
        "on_behalf_of": BRIDGE_CUSTOMER,
        "source": {
            "payment_rail": "solana",
            "currency": "usdc",
            "from_address": from_address,
        },
        "destination": {
            "payment_rail": "polygon",
            "currency": "usdc",
            "to_address": to_address,
        }
    })

    print(data)

    response = requests.request(
        "POST",
        url,
        headers=headers,
        data=data
    )

    print(response.text)

    res_data = json.loads(response.text)


    return Bridge(
        amount=int(float(res_data["source_deposit_instructions"]["amount"])),
        id=res_data["id"],
        id_key=headers["Idempotency-Key"],
        to_address=res_data["source_deposit_instructions"]["to_address"],
        from_address=res_data["source_deposit_instructions"]["from_address"],
    )

def _get_random_string(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_transfer(id: str):
    headers = {
      'Content-Type': 'application/json',
      'Api-Key': BRIDGE_KEY,
    }
    url = f'https://api.bridge.xyz/v0/transfers/{id}'
    return requests.request(
        "GET",
        url,
        headers=headers,
    )
