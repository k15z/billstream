import enum
from pydantic import BaseModel


class ToolKind(enum.Enum):
    REQUEST_THEN_RESPONSE = "REQUEST_THEN_RESPONSE"


class RequestPaymentResponse(BaseModel):
    id: str
    address: str
    amount: int
