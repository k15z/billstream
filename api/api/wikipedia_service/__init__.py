import uuid
import fastapi
from pydantic import BaseModel
from api.payment import PaymentRequest
import wikipedia

router = fastapi.APIRouter(
    prefix="/wikipedia",
    tags=["wikipedia"],
)


class WikipediaRequest(BaseModel):
    query: str


class WikipediaResponse(BaseModel):
    message: str


id_to_request = {}
id_to_payment_request = {}


@router.post("/spec")
async def spec(request: WikipediaRequest) -> WikipediaResponse:
    """Wikipedia API.

    Given a query, returns the article summary from Wikipedia.
    """
    raise NotImplementedError("This is a stub.")


@router.post("/")
async def post(request: WikipediaRequest) -> PaymentRequest:
    id = str(uuid.uuid4())
    id_to_request[id] = request
    id_to_payment_request[id] = PaymentRequest(id=id, address="0x54F89EeD99D0E9a6154c4207F9bF4e16FB351ED6", amount=1)
    return id_to_payment_request[id]


@router.get("/")
async def get(id: str, proof: str) -> WikipediaResponse:
    if not id_to_payment_request[id].was_paid(proof):
        raise fastapi.HTTPException(status_code=402, detail="Payment not received")
    pages = wikipedia.search(id_to_request[id].query)
    print(pages, pages[0])
    summary = wikipedia.page(pages[0]).content
    return WikipediaResponse(message=summary[:10_000])
