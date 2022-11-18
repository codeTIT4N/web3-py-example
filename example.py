from web3 import Web3
from dotenv import load_dotenv
load_dotenv()
import os
import json
abi_file = open('./abis/erc20.json')
abi = json.load(abi_file)
w3 = Web3(Web3.HTTPProvider('https://matic-mumbai.chainstacklabs.com'))

pvt_key = os.getenv("PVT_KEY")
signer = w3.eth.account.from_key('0x'+pvt_key)
pub_key=signer.address
print('Public key/Address',pub_key)

#getting contract instance
contract_address='0xfEc014B41506430F055ceff9A007e690D409b304'
erc20_contract =  w3.eth.contract(address=contract_address, abi=abi)
# calling simple read functions
balBef = erc20_contract.functions.balanceOf(pub_key).call()
print('ERC20 Balance before:',balBef)

#inject middleware
from web3.middleware import geth_poa_middleware
w3.middleware_onion.inject(geth_poa_middleware, layer=0)


# MATIC mumbai chain
chain_id = 80001
nonce = w3.eth.getTransactionCount(pub_key)
send_to='0xc9D506209f57948a0C0df6ED45621Fb47572Af99'
transfer_amt=w3.toWei(1,'ether'); # 1 token

try:
    # creating a transaction
    transfer_txn = erc20_contract.functions.transfer(send_to,transfer_amt).buildTransaction({ "chainId":chain_id, "from":pub_key, "nonce":nonce})
    # signing transaction with pvt key
    signed_tx = w3.eth.account.sign_transaction(transfer_txn, pvt_key)
    # sending the transaction
    txn_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print('Transaction hash:',txn_hash.hex())
    #wait for the transaction to process
    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

except Exception as err: 
    print('Transaction Error:',err)


balAfter = erc20_contract.functions.balanceOf(pub_key).call()
print('ERC20 Balance after:',balAfter)