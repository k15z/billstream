from typing import Any
from pydantic import BaseModel

class Wallet(BaseModel):
    def pay(self, request: dict) -> str:
        raise NotImplementedError("This is a stub.")
