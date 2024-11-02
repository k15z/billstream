import uuid
import fastapi
from pydantic import BaseModel
from api.payment import PaymentRequest

router = fastapi.APIRouter(
    prefix="/calendar",
    tags=["calendar"],
)


class CalendarRequest(BaseModel):
    query: str


class CalendarResponse(BaseModel):
    message: str


id_to_request = {}
id_to_payment_request = {}


@router.post("/spec")
async def spec(request: CalendarRequest) -> CalendarResponse:
    """Calendar API.

    Given a query related to the calendar, return a response. Examples include:
    - "What's next on my calendar?"
    - "Schedule a meeting with John Doe on Tuesday at 2pm."

    Note: This API is not yet implemented and should not be called.
    """
    raise NotImplementedError("This is a stub.")


@router.post("/")
async def post(request: CalendarRequest) -> CalendarResponse:
    id = str(uuid.uuid4())
    id_to_request[id] = request
    id_to_payment_request[id] = PaymentRequest(id=id, address="0x123", amount=100)
    return id_to_payment_request[id]


@router.get("/")
async def get(id: str) -> CalendarResponse:
    if not id_to_payment_request[id].was_paid():
        raise fastapi.HTTPException(status_code=402, detail="Payment not received")
    return CalendarResponse(message=f"Not implemented yet!")
