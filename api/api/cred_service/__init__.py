import uuid
import fastapi
from pydantic import BaseModel
from api.payment import PaymentRequest
import requests

router = fastapi.APIRouter(
    prefix="/credprotocol",
    tags=["credprotocol"],
)


class CredReportRequest(BaseModel):
    address: str


class CredReportResponse(BaseModel):
    total_asset_usd: float


id_to_request = {}
id_to_payment_request = {}


@router.post("/spec")
async def spec(request: CredReportRequest) -> CredReportResponse:
    """Cred Protocol API.

    This function takes a crypto address and returns the total balance (USD) on Ethereum.
    """
    raise NotImplementedError("This is a stub.")


@router.post("/")
async def post(request: CredReportRequest) -> PaymentRequest:
    id = str(uuid.uuid4())
    id_to_request[id] = request
    id_to_payment_request[id] = PaymentRequest(id=id, address="0x54F89EeD99D0E9a6154c4207F9bF4e16FB351ED6", amount=1)
    return PaymentRequest(id=id, address="0x123", amount=100)


@router.get("/")
async def get(id: str) -> CredReportResponse:
    if not id_to_payment_request[id].was_paid():
        raise fastapi.HTTPException(status_code=402, detail="Payment not received")
    
    cred_protocol_api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNzMzMTYyOTUyfQ.WilIo1tso8kIlmM0rlWjSv_BW8Ata3oIW5Wa8C3os8o"
    address = id_to_request[id].address
    chain_id = 1 # Ethereum mainnet
    url = f"https://api.credprotocol.com/report/address/{address}/chain/{chain_id}"
    headers = {
        "Authorization": f"Bearer {cred_protocol_api_key}"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    print(data)
    total_asset_usd = data['report']["summary"]["total_asset_usd"]

    return CredReportResponse(total_asset_usd=total_asset_usd)
