import uuid
import fastapi
from pydantic import BaseModel
from api._types import RequestPaymentResponse

router = fastapi.APIRouter(
    prefix="/example",
    tags=["example"],
)


class ExampleRequest(BaseModel):
    name: str


class ExampleResponse(BaseModel):
    message: str


id_to_request = {}


@router.post("/")
async def pay(request: ExampleRequest) -> RequestPaymentResponse:
    id = str(uuid.uuid4())
    id_to_request[id] = request
    return RequestPaymentResponse(id=id, address="0x123", amount=100)


@router.get("/")
async def get_example(id: str) -> ExampleResponse:
    request = id_to_request[id]
    # process request
    return ExampleResponse(message=f"Hello, {request.name}!")
