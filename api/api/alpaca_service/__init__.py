import uuid
import fastapi
from pydantic import BaseModel
from api.payment import PaymentRequest
import requests

router = fastapi.APIRouter(
    prefix="/stocks",
    tags=["stocks"],
)


class AlpacaRequest(BaseModel):
    query: str


class AlpacaResponse(BaseModel):
    message: str


id_to_request = {}
id_to_payment_request = {}


@router.post("/spec")
async def spec(request: AlpacaRequest) -> AlpacaResponse:
    """Alpaca API.

    Given a query related to the stock market, return a response. Examples include:
    - "What is the price of Tesla?"
    - "What is the price of Bitcoin?"
    - "What is the price of Apple?"
    - "what is the top performing stock today?"

    Note: This API is not yet implemented and should not be called.
    """
    raise NotImplementedError("This is a stub.")


@router.post("/")
async def post(request: AlpacaRequest) -> AlpacaResponse:
    id = str(uuid.uuid4())
    id_to_request[id] = request
    id_to_payment_request[id] = PaymentRequest(id=id, address="0x54F89EeD99D0E9a6154c4207F9bF4e16FB351ED6", amount=1)
    return id_to_payment_request[id]


@router.get("/")
async def get(id: str) -> AlpacaResponse:
    if not id_to_payment_request[id].was_paid():
        raise fastapi.HTTPException(status_code=402, detail="Payment not received")
    return AlpacaResponse(message=f"Not implemented yet!")
