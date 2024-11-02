import uuid
import fastapi
from pydantic import BaseModel
from api._types import RequestPaymentResponse
import requests

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


@router.get("/weather")
async def get_weather(city: str) -> ExampleResponse:

    weather_api_key = "f093c2b5da3b49dfa9104019240211"
    response = requests.get(f"https://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}&aqi=no")
    weather_data = response.json()
    weather_condition = weather_data['current']['condition']['text']
    
    return ExampleResponse(message=f"The weather in {city} is {weather_condition}")
