import uuid
import fastapi
from pydantic import BaseModel
from api.payment import PaymentRequest
import requests

router = fastapi.APIRouter(
    prefix="/greeting",
    tags=["greeting"],
)


class GreetingRequest(BaseModel):
    name: str


class GreetingResponse(BaseModel):
    message: str


id_to_request = {}
id_to_payment_request = {}


@router.post("/spec")
async def spec(request: GreetingRequest) -> GreetingResponse:
    """Example API.

    Given the user's name, return a greeting.
    """
    raise NotImplementedError("This is a stub.")


@router.post("/")
async def post(request: GreetingRequest) -> PaymentRequest:
    id = str(uuid.uuid4())
    id_to_request[id] = request
    id_to_payment_request[id] = PaymentRequest(id=id, address="0x123", amount=100)
    return id_to_payment_request[id]


@router.get("/")
async def get(id: str) -> GreetingResponse:
    if not id_to_payment_request[id].was_paid():
        raise fastapi.HTTPException(status_code=402, detail="Payment not received")
    request = id_to_request[id]
    return GreetingResponse(message=f"Hello, {request.name}!")
