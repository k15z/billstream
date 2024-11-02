from typing import Any

class Wallet:
    def pay(self, payment_instructions: Any) -> None:
        raise NotImplementedError("This is a stub.")

class PrivyWallet(Wallet):
    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def pay(self, payment_instructions: Any) -> None:
        pass
