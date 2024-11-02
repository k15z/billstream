import enum
from pydantic import BaseModel


class PaymentRequest(BaseModel):
    id: str
    address: str
    amount: int

    def was_paid(self):
        # TODO: Validate this.
        return True
