import json
from base64 import b64decode, b64encode
from solathon import Client, Transaction, PublicKey, Keypair
from solathon.core.instructions import transfer
from sdk.payments.privy import sign_message

client = Client("https://api.devnet.solana.com")

def transfer_sol(amount, to, sender):
    recent_blockhash=client.get_latest_blockhash().blockhash

    instruction = transfer(
        from_public_key=PublicKey(sender),
        to_public_key=PublicKey(to),
        lamports=amount
    )

    transaction = Transaction(
        instructions=[instruction],
        signers=[PublicKey(sender)],
        recent_blockhash=recent_blockhash,
    )

    txn_bytes = transaction.compile_transaction()
    response = sign_message(sender, txn_bytes)

    print(response.text)
    signature: str = json.loads(response.text)["data"]["signature"]

    signed = Transaction(
        instructions=[instruction],
        signers=[PublicKey(sender)],
        recent_blockhash=recent_blockhash,
    )

    signed.sign([b64decode(signature.encode('utf-8'))])

    serialized = signed.serialize()

    return client.build_and_send_request(
        "sendTransaction",
        [signed.serialize(), {"encoding": "base64"}]
    )
