from solcx import compile_standard, install_solc
import datetime 
import threading
import asyncio
import requests
import time
import os
import sys
import ctypes
import pyperclip as pc
install_solc('0.8.0')

with open("ERC20TOKEN.sol", "r") as file:
    erc20token_file = file.read()

import json
...

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"ERC20TOKEN.sol": {"content": erc20token_file}},
        "settings": {
             "optimizer": {
             "enabled": bool(True),
             "runs": 200
            },
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"] # output needed to interact with and deploy contract 
                }
            }
        },
    },
    solc_version="0.8.0",
)
#print(compiled_sol)
#with open("compiled_code.json", "w") as file:
#json.dump(compiled_sol, file)

# get bytecode
# ERC20TOKEN = mean contract function you want deploy in sol code
bytecode = compiled_sol["contracts"]["ERC20TOKEN.sol"]["ERC20TOKEN"]["evm"]["bytecode"]["object"]# get abi
abi = json.loads(compiled_sol["contracts"]["ERC20TOKEN.sol"]["ERC20TOKEN"]["metadata"])["output"]["abi"]

#set title
ctypes.windll.kernel32.SetConsoleTitleW("Deploy ERC20TOKEN Standart On Blockchain Network")
print('Deploy ERC20TOKEN Standart On Blockchain Network With Python')
print('This Support Tesnet & Mainnet Ethereum, Binance Smart Chain, Polygon')
print('Polygon zkEVM, Arbitrum, Optimism, Avalanche, zkSync Era, & Base')
print('You Need Gas Fee Depends On Your Choose Blockchain Network Like ETH/BNB/MATIC/OTHER')

# For connecting to web3
from web3 import Web3
#bsc = "https://bsc-testnet.publicnode.com" #rpc bsctesnet custom #you can find rpc on chainlist.org
inputrpc = str(input("Input Url RPC/Node Blockchain Network : "))
web3 = Web3(Web3.HTTPProvider(inputrpc))
#chain_id = 97 #you can find chainid on chainlist.org
chain_id = int(input("Input Chain ID Blockchain Network : "))

#connecting web3
if  web3.isConnected() == True:
    print("web3 connected...\n")
else :
    print("error connecting please try again...")

address = web3.toChecksumAddress(input("Enter your address 0x...: "))
private_key = input("Enter your privatekey abcde12345...: ")
name_ = str(input("Enter token name example CAT : "))
symbol_ = str(input("Enter token symbol example CT : "))
totalSupply_ = int(input("Enter total supply token example 1000000 : "))
Contract = web3.eth.contract(abi=abi, bytecode=bytecode)
# Get the number of latest transaction
nonce = web3.eth.getTransactionCount(address)

#Get balance account
def UpdateBalance():
    balance = web3.eth.get_balance(address)
    balance_bnb = web3.fromWei(balance,'ether')
    print('Your Balance' ,balance_bnb, 'ETH/BNB/MATIC/OTHER')
    
UpdateBalance()

#estimate gas limit contract
gas_tx = Contract.constructor(name_, symbol_, totalSupply_).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": web3.eth.gas_price,
        "from": address,
        "nonce": nonce
    }
)
gasAmount = web3.eth.estimateGas(gas_tx)

# build transaction
transaction = Contract.constructor(name_, symbol_, totalSupply_).buildTransaction(
    {
        "chainId": chain_id,
        "gas": gasAmount,
        "gasPrice": web3.eth.gas_price,
        "from": address,
        "nonce": nonce
    }
)
# Sign the transaction
sign_transaction = web3.eth.account.sign_transaction(transaction, private_key)
# Send the transaction
transaction_hash = web3.eth.send_raw_transaction(sign_transaction.rawTransaction)
# Wait for the transaction to be mined, and get the transaction receipt
#get transaction hash
txid = str(web3.toHex(transaction_hash))
transaction_receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)
print('Transaction Success Contract deployed! TX-ID & Contract Address Copied To Clipboard')
print('TX-ID : '+txid+ ' & ' 'Contract Address : '+transaction_receipt.contractAddress)
pc.copy('TX-ID : '+txid+ ' & ' 'Contract Address : '+transaction_receipt.contractAddress)
#print('https://testnet.bscscan.com/address/'+transaction_receipt.contractAddress)
#pc.copy('https://testnet.bscscan.com/tx/'+txid+ ' && ' +'https://testnet.bscscan.com/address/'+transaction_receipt.contractAddress)
print('update current balance in 30 second...')
time.sleep(30)
UpdateBalance() #get latest balance
print('will close automatically in 30 second...')
time.sleep(30)