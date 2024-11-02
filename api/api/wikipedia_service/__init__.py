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
    id_to_payment_request[id] = PaymentRequest(id=id, address="0x123", amount=100)
    return id_to_payment_request[id]


@router.get("/")
async def get(id: str) -> WikipediaResponse:
    if not id_to_payment_request[id].was_paid():
        raise fastapi.HTTPException(status_code=402, detail="Payment not received")
    pages = wikipedia.search(id_to_request[id].query)
    print(pages, pages[0])
    summary = wikipedia.page(pages[0]).content
    return WikipediaResponse(message=summary)
