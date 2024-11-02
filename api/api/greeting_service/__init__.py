import uuid
import fastapi
from pydantic import BaseModel
from api._types import RequestPaymentResponse
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
@router.post("/spec")
async def spec(request: GreetingRequest) -> GreetingResponse:
    """Example API.

    Given the user's name, return a greeting.
    """
    raise NotImplementedError("This is a stub.")



@router.post("/")
async def post(request: GreetingRequest) -> RequestPaymentResponse:
    id = str(uuid.uuid4())
    id_to_request[id] = request
    return RequestPaymentResponse(id=id, address="0x123", amount=100)


@router.get("/")
async def get(id: str) -> GreetingResponse:
    request = id_to_request[id]
    # process request
    return GreetingResponse(message=f"Hello, {request.name}!")
