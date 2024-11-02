from dotenv import load_dotenv
from sdk.payments import bridge
from sdk.payments.solana import transfer_sol, transfer_usdc
from sdk.payments.bridge import create_bridge, get_transfer
import json

load_dotenv()

sender = "FbG8R8Upa3d19gFzc9fMwPzzCNTzn4hLprCCaYSK1knN"

usdc_eth_to_address = "0x54F89EeD99D0E9a6154c4207F9bF4e16FB351ED6"

bridge = create_bridge("1.00", sender, usdc_eth_to_address, "N0J9N7" )
print(bridge)

# result = transfer_usdc(amount=bridge.amount, to=bridge.to_address, sender=bridge.from_address)

# print("txn:")
# print(result)
# print()

response = get_transfer(bridge.id)

print(json.loads(response.text))
