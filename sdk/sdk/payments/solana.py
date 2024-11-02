import json
from base64 import b64decode
from sdk.payments.privy import sign_message
from solana.rpc.api import Client

from solders.message import MessageV0, to_bytes_versioned, Message
from solders.system_program import CreateAccountParams, TransferParams, transfer, create_account
from solders.transaction import VersionedTransaction, Transaction
from solders.pubkey import Pubkey
from solders.null_signer import NullSigner
from solders.signature import Signature
from spl.token.constants import TOKEN_PROGRAM_ID
import spl.token.instructions as spl_token

client = Client("https://api.mainnet-beta.solana.com")

usdc = Pubkey.from_string("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v")

def transfer_usdc(amount: float, to: str, sender: str):
    print('starting_transfer')
    print()

    to_key = Pubkey.from_string(to)
    sender_key = Pubkey.from_string(sender)

    sender_token_address = spl_token.get_associated_token_address(sender_key, usdc)
    recipient_token_address = spl_token.get_associated_token_address(to_key, usdc)

    ix = spl_token.transfer_checked(
        spl_token.TransferCheckedParams(
            program_id=TOKEN_PROGRAM_ID,
            source=sender_token_address,
            dest=recipient_token_address,
            mint=usdc,
            owner=sender_key,
            amount=int(amount * (10**6)),
            decimals=6,
        )
    )

    blockhash = client.get_latest_blockhash().value.blockhash
    msg = Message.new_with_blockhash([ix], sender_key, blockhash)
    tx = Transaction.new_unsigned(msg)

    serialized = bytes(tx)
    deserialized = Transaction.from_bytes(serialized)
    assert deserialized == tx

    deserialized_message = deserialized.message
    response = sign_message(sender, to_bytes_versioned(deserialized_message))
    signature: str = json.loads(response.text)["data"]["signature"]

    sigs = deserialized.signatures
    sigs[0] = Signature.from_bytes(b64decode(signature.encode('utf-8')))
    deserialized.signatures = sigs

    return client.send_transaction(deserialized)



def transfer_sol(amount: int, to: str, sender: str):
    to_key = Pubkey.from_string(to)
    sender_key = Pubkey.from_string(sender)

    ix = transfer(
        TransferParams(
            from_pubkey=sender_key, to_pubkey=to_key, lamports=amount
        )
    )
    blockhash = client.get_latest_blockhash().value.blockhash

    msg = MessageV0.try_compile(
        payer=sender_key,
        instructions=[ix],
        address_lookup_table_accounts=[],
        recent_blockhash=blockhash,
    )
    tx = VersionedTransaction(msg, (NullSigner(sender_key),))

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
