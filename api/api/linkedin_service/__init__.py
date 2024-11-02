import os
import uuid
import fastapi
from pydantic import BaseModel
from api.payment import PaymentRequest
import requests
from typing import Optional, Union
from dotenv import load_dotenv

load_dotenv()

router = fastapi.APIRouter(
    prefix="/linkedin",
    tags=["linkedin"],
)


class LinkedinRequest(BaseModel):
    profile_name: str
    message: Optional[str] = None


class Profile(BaseModel):
    id: str
    name: str
    location: str
    headline: str


class LinkedinResponse(BaseModel):
    profiles: list[Profile]


class LinkedinMessageResponse(BaseModel):
    message: str


id_to_request = {}
id_to_payment_request = {}


@router.post("/spec")
async def spec(
    request: LinkedinRequest,
) -> Union[LinkedinResponse, LinkedinMessageResponse]:
    """LinkedIn API.

    This finds the specified profile name on LinkedIn. If message is not set, then
    it simply returns a list of profiles that match. If message is set, then it
    attempts to start a conversation with the first match.
    """
    raise NotImplementedError("This is a stub.")


@router.post("/")
async def post(request: LinkedinRequest) -> PaymentRequest:
    id = str(uuid.uuid4())
    id_to_request[id] = request
    id_to_payment_request[id] = PaymentRequest(id=id, address="0x54F89EeD99D0E9a6154c4207F9bF4e16FB351ED6", amount=1)
    return id_to_payment_request[id]


@router.get("/")
async def get(id: str, proof: str) -> Union[LinkedinResponse, LinkedinMessageResponse]:
    if not id_to_payment_request[id].was_paid(proof):
        raise fastapi.HTTPException(status_code=402, detail="Payment not received")
    profile_name = id_to_request[id].profile_name
    url = "https://svc.sandbox.anon.com/actions/linkedin/search"

    payload = {
        "profileName": profile_name,
        "appUserId": "kevz@lightspark.com",
    }
    headers = {
        "Authorization": f"Bearer {os.getenv('ANON_API_KEY')}",
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    profiles = []
    print(response.text)
    for profile in response.json()["profiles"]:
        profiles.append(Profile(**profile))

    if id_to_request[id].message:
        url = "https://svc.sandbox.anon.com/actions/linkedin/createConversation"

        payload = {
            "profileId": profiles[0].id,
            "appUserId": "kevz@lightspark.com",
            "message": id_to_request[id].message,
        }
        response = requests.request("POST", url, json=payload, headers=headers)
        return LinkedinMessageResponse(message=id_to_request[id].message)

    return LinkedinResponse(profiles=profiles)
