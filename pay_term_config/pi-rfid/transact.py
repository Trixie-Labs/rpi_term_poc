#!/usr/bin/env python

import sys
from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.exceptions import TransactionNotFound
import os
from dotenv import load_dotenv

load_dotenv('/home/vitor/pay_term_config/pay.txt')

INFURA_URL = os.getenv('INFURA_URL')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')
TERM_ADDRESS = os.getenv('TERM_ADDRESS')
print(INFURA_URL)
print(CONTRACT_ADDRESS)
print(TERM_ADDRESS)

# ERC-20 contract address and ABI (Replace with your contract details)
contract_abi = [
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "receiver",
                "type": "address",
            }
        ],
        "name": "pay",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    }
]

# Ethereum sender account private key (Passed as a parameter)
private_key = sys.argv[1]
print(private_key)

# Initialize Web3 instance
w3 = Web3(Web3.HTTPProvider(INFURA_URL))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Validate the private key
if not w3.is_address(TERM_ADDRESS):
    print("Invalid recipient address")
    sys.exit(1)

if not w3.is_address(CONTRACT_ADDRESS):
    print("Invalid contract address")
    sys.exit(1)

try:
    private_key = Web3.to_hex(Web3.to_bytes(hexstr=private_key))
    sender_account = w3.eth.account.from_key(private_key)
    sender_address = sender_account.address
except ValueError:
    print("Invalid private key")
    sys.exit(1)

# Initialize contract instance
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

print(contract.functions)

# Build the transaction
transaction = {
    "value": 0,
    "gas": 200000,  # Adjust gas limit as needed
    "gasPrice": w3.to_wei("20", "gwei"),  # Adjust gas price as needed
    "nonce": w3.eth.get_transaction_count(sender_address),
}

# Build the function call to transfer tokens
data = contract.functions.pay(TERM_ADDRESS).build_transaction(transaction)

# Sign the transaction
signed_transaction = w3.eth.account.sign_transaction(data, private_key)

# Send the transaction
try:
    tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    print(f"Transaction sent with hash: {tx_hash.hex()}")
except Exception as e:
    print(f"Transaction failed: {e}")
