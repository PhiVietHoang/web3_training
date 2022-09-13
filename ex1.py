from web3 import HTTPProvider
from web3 import Web3
from web3.middleware import geth_poa_middleware
import time
import json

provider_url = "https://bsc-dataseed4.binance.org/" # rpc link
web3 = Web3(HTTPProvider(provider_url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

latestBlocknumber = web3.eth.blockNumber
sum = 0
for i in range (100):
    sum = sum + web3.eth.get_block_transaction_count(latestBlocknumber-i)
average = sum/100
print (average)

string = {
  "fromBlock":(latestBlocknumber-99),
  "toBlock":latestBlocknumber,
  "averageTransactions": average
  } 

with open('ex1.json', 'w') as myfile:
  json.dump(string, myfile)

