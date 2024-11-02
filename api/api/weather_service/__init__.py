import uuid
import fastapi
from pydantic import BaseModel
from api._types import RequestPaymentResponse
import requests

router = fastapi.APIRouter(
    prefix="/weather",
    tags=["weather"],
)



class WeatherRequest(BaseModel):
    weather: str


class WeatherResponse(BaseModel):
    condition: str


id_to_request = {}

@router.post("/spec")
async def spec(request: WeatherRequest) -> WeatherResponse:
    """Weather API.

    This function takes the city name and returns the weather condition.
    """
    raise NotImplementedError("This is a stub.")


@router.post("/")
async def post(request: WeatherRequest) -> RequestPaymentResponse:
    id = str(uuid.uuid4())
    id_to_request[id] = request
    return RequestPaymentResponse(id=id, address="0x123", amount=100)


@router.get("/")
async def get(id: str) -> WeatherResponse:
    weather_api_key = "f093c2b5da3b49dfa9104019240211"
    city = id_to_request[id].weather
    response = requests.get(f"https://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}&aqi=no")
    weather_data = response.json()
    weather_condition = weather_data['current']['condition']['text']
    return WeatherResponse(condition=weather_condition)
