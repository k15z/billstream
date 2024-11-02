import json
from base64 import b64decode, b64encode
from sdk.payments.privy import sign_message
from solana.rpc.api import Client
import solders.system_program as sp

from solders.hash import Hash
from solders.keypair import Keypair
from solders.message import MessageV0, to_bytes_versioned
from solders.system_program import TransferParams, transfer
from solders.transaction import VersionedTransaction
from solders.pubkey import Pubkey
from solders.null_signer import NullSigner
from solders.signature import Signature

# Note that Keypair() will always give a public key that is valid for users


client = Client("https://api.devnet.solana.com")

def transfer_sol(amount, to, sender):
    toKey = Pubkey.from_string(to)
    senderKey = Pubkey.from_string(sender)

    ix = transfer(
        TransferParams(
            from_pubkey=senderKey, to_pubkey=toKey, lamports=amount
        )
    )
    blockhash = client.get_latest_blockhash().value.blockhash

    msg = MessageV0.try_compile(
        payer=senderKey,
        instructions=[ix],
        address_lookup_table_accounts=[],
        recent_blockhash=blockhash,
    )
    tx = VersionedTransaction(msg, (NullSigner(senderKey),))

    serialized = bytes(tx)
    deserialized = VersionedTransaction.from_bytes(serialized)
    assert deserialized == tx

    deserialized_message = deserialized.message
    response = sign_message(sender, to_bytes_versioned(deserialized_message))
    signature: str = json.loads(response.text)["data"]["signature"]

    sigs = deserialized.signatures
    sigs[0] = Signature.from_bytes(b64decode(signature.encode('utf-8')))
    deserialized.signatures = sigs

    return client.send_transaction(deserialized)
