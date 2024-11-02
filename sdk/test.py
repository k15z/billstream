from dotenv import load_dotenv
from sdk.payments.solana import transfer_sol

load_dotenv()

receiver = "7EEJrsdnm9heACSxakCcvUzxkWjno3FaCNdzcBCEZPFv"
sender = "FbG8R8Upa3d19gFzc9fMwPzzCNTzn4hLprCCaYSK1knN"

# This is the amount in lamports
amount = 1250000

result = transfer_sol(amount=amount, to=receiver, sender=sender)
print("Transaction response:", result)
