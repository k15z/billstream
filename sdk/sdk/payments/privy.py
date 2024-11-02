import os
import json
from base64 import b64encode
import requests
from dotenv import load_dotenv

load_dotenv()

PRIVY_APP_ID = os.environ.get("PRIVY_APP_ID")
PRIVY_APP_SECRET = os.environ.get("PRIVY_APP_SECRET")

headers = {
  'privy-app-id': PRIVY_APP_ID,
  'Content-Type': 'application/json',
  'Authorization': f'Basic {b64encode(f"{PRIVY_APP_ID}:{PRIVY_APP_SECRET}".encode("utf-8")).decode("ascii")}',
}

def create_user():
    url = 'https://auth.staging.privy.io/api/v1/wallets/create_wallet'
    return requests.request("POST", url, headers=headers, data=json.dumps({}))

def _to_signature_request(address: str, message: bytes, method: str):
    payload = {
        "address": address,
        "chain_type": "solana",
        "method": method,
        "params": {
            "encoding": "base64"
        }
    }

    if method == "signMessage":
        payload["params"]["message"] = b64encode(message).decode("ascii")
    elif method == "signTransaction":
        payload["params"]["transaction"] = b64encode(message).decode("ascii")

    return json.dumps(payload)

def sign_message(address: str, message: bytes):
    url = "https://auth.staging.privy.io/api/v1/wallets/rpc"

    return requests.request(
        "POST",
        url,
        headers=headers,
        data=_to_signature_request(
            address,
            message,
            "signMessage"
        )
    )
