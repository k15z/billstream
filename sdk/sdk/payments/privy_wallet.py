from pydantic import BaseModel
from sdk.payments.bridge import create_bridge
from sdk.payments.solana import transfer_usdc
from sdk.wallets import Wallet

class PrivyWallet(Wallet):
    address: str

    def pay(self, request: dict) -> str:
        bridge = create_bridge(
            amount=str(request["amount"]),
            from_address=self.address,
            to_address=request["address"],
            id_key=None
        )

        print(bridge)

        transfer = transfer_usdc(
            amount=bridge.amount,
            to=bridge.to_address,
            sender=bridge.from_address,
        )

        print(transfer)

        return f"{transfer.value.to_json()}:{bridge.id}"
