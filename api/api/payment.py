import enum
import json
from pydantic import BaseModel
import requests
from solana.rpc.api import Client
from solders.signature import Signature
import os
from dotenv import load_dotenv


class PaymentRequest(BaseModel):
    id: str
    address: str
    amount: float

    def was_paid(self, proof: str):
        [txid, bridgeid] = proof.split(':')
        print(txid, bridgeid)
        tx = get_tx(txid)
        print(tx)
        bridge = get_transfer(bridgeid)
        print(bridge)
        return True


def get_transfer(id: str):
    load_dotenv()
    BRIDGE_KEY = os.environ.get("BRIDGE_KEY")
    headers = {
      'Content-Type': 'application/json',
      'Api-Key': BRIDGE_KEY,
    }
    url = f'https://api.bridge.xyz/v0/transfers/{id}'
    res =  requests.request(
        "GET",
        url,
        headers=headers,
    )
    return json.loads(res.text)


def get_tx(id: str):
    client = Client("https://api.mainnet-beta.solana.com")
    return client.get_signature_statuses([Signature.from_json(id)])
