import os
import uuid
import fastapi
from pydantic import BaseModel
from api.payment import PaymentRequest
import requests
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

router = fastapi.APIRouter(
    prefix="/nytimes",
    tags=["nytimes"],
)


class NYTimesRequest(BaseModel):
    category: Optional[str] = "us"


class Article(BaseModel):

    title: str
    abstract: str


class NYTimesResponse(BaseModel):
    articles: list[Article]


id_to_request = {}
id_to_payment_request = {}


@router.post("/spec")
async def spec(request: NYTimesRequest) -> NYTimesResponse:
    """NYTimes API.

    This fetches the top news stories for a given category. If not set,
    it should default to "us". Other valid values are:

        arts, automobiles, books/review, business, fashion, food, health, home,
        insider, magazine, movies, nyregion, obituaries, opinion, politics, realestate,
        science, sports, sundayreview, technology, theater, t-magazine, travel,
        upshot, us, and world
    
    If you want news but aren't sure what category, you can just use "us".
    """
    raise NotImplementedError("This is a stub.")


@router.post("/")
async def post(request: NYTimesRequest) -> PaymentRequest:
    id = str(uuid.uuid4())
    id_to_request[id] = request
    id_to_payment_request[id] = PaymentRequest(id=id, address="0x123", amount=100)
    return PaymentRequest(id=id, address="0x123", amount=100)


@router.get("/")
async def get(id: str) -> NYTimesResponse:
    if not id_to_payment_request[id].was_paid():
        raise fastapi.HTTPException(status_code=402, detail="Payment not received")
    category = id_to_request[id].category
    api_key = os.getenv("NYTIMES_API_KEY")
    response = requests.get(
        f"https://api.nytimes.com/svc/topstories/v2/{category}.json?api-key={api_key}"
    )
    data = response.json()
    articles = []
    for article in data["results"]:
        articles.append(Article(title=article["title"], abstract=article["abstract"]))
    return NYTimesResponse(articles=articles)
