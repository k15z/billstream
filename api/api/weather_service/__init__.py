import uuid
import fastapi
from pydantic import BaseModel
from api.payment import PaymentRequest
import requests

router = fastapi.APIRouter(
    prefix="/weather",
    tags=["weather"],
)


class WeatherRequest(BaseModel):
    city: str


class WeatherResponse(BaseModel):
    condition: str


id_to_request = {}
id_to_payment_request = {}


@router.post("/spec")
async def spec(request: WeatherRequest) -> WeatherResponse:
    """Weather API.

    This function takes the city name and returns the weather condition.
    """
    raise NotImplementedError("This is a stub.")


@router.post("/")
async def post(request: WeatherRequest) -> PaymentRequest:
    id = str(uuid.uuid4())
    id_to_request[id] = request
    id_to_payment_request[id] = PaymentRequest(id=id, address="0x54F89EeD99D0E9a6154c4207F9bF4e16FB351ED6", amount=1)
    return id_to_payment_request[id]

@router.get("/")
async def get(id: str, proof: str) -> WeatherResponse:
    if not id_to_payment_request[id].was_paid(proof):
        raise fastapi.HTTPException(status_code=402, detail="Payment not received")
    weather_api_key = "f093c2b5da3b49dfa9104019240211"
    city = id_to_request[id].city
    response = requests.get(
        f"https://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}&aqi=no"
    )
    weather_data = response.json()
    weather_condition = weather_data["current"]["condition"]["text"]
    return WeatherResponse(condition=weather_condition)
