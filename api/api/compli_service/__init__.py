import uuid
import fastapi
from pydantic import BaseModel
from api.payment import PaymentRequest
import requests

router = fastapi.APIRouter(
    prefix="/compliapi",
    tags=["compliapi"],
)


class ComplianceRequest(BaseModel):
    address: str


class ComplianceResponse(BaseModel):
    sanctioned: bool


id_to_request = {}
id_to_payment_request = {}


@router.post("/spec")
async def spec(request: ComplianceRequest) -> ComplianceResponse:
    """Compli API.

    This function takes a crypto address and returns whether it's on an OFAC sanctions list.
    """
    raise NotImplementedError("This is a stub.")


@router.post("/")
async def post(request: ComplianceRequest) -> PaymentRequest:
    id = str(uuid.uuid4())
    id_to_request[id] = request
    id_to_payment_request[id] = PaymentRequest(id=id, address="0x54F89EeD99D0E9a6154c4207F9bF4e16FB351ED6", amount=1)
    return PaymentRequest(id=id, address="0x123", amount=100)


@router.get("/")
async def get(id: str, proof: str) -> ComplianceResponse:
    if not id_to_payment_request[id].was_paid(proof):
        raise fastapi.HTTPException(status_code=402, detail="Payment not received")
    
    compli_api_key = "b99d8a3b75b4ffd9236bdb5739dedec5d5ebaea2"
    address = id_to_request[id].address
    url = f"https://compliapi.com/api/v1/ofac/onchain/{address}/"
    headers = {
        "Authorization": f"Token {compli_api_key}"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    print(data)
    sanctioned = data.get("sanctioned")

    return ComplianceResponse(sanctioned=sanctioned)
