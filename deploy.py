from gettext import translation
from inspect import trace
import json
import os
from solcx import compile_standard
import json
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# reading the solidity file
with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# compile our solidity
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.0",
)

# save the compiled sol
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get the bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get the abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# for connecting to ganache or rinkaby or mainnet
w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/eacef39c4e8742ebb26203668498dfe1")
)
chain_id = 4
my_address = "0x876dCA9aEf9D8A648A86a5De8c9f25410fA251A4"
private_key = os.getenv("PRIVATE_KEY")  # always add 0x in front

# create a contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# get latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# 1. build a transaction
print("deploying contract...")
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)
# 2. sign a transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
# 3. send a transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("deployed contract!")

# ----------------------------------------------------------------------------------------------------
# working with contracts (interacting with contracts)
# 1. contract address
# 2. contract abi
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# call -> simulate making call and getting the return value
# transact -> actually make a state change

# initial vallue of the favoraiteNumber
print(simple_storage.functions.retrive().call())
print(simple_storage.functions.store(15).call())  # will not make the state change

# setting the favoraiteNumber
print("updating contract...")
store_transaction = simple_storage.functions.store(123).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1,  # already used once before
    }
)
signed_store_transaction = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
send_store_transaction = w3.eth.send_raw_transaction(
    signed_store_transaction.rawTransaction
)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_transaction)
print("updated contract!")

# final value of favoraiteNumber
print(simple_storage.functions.retrive().call())
