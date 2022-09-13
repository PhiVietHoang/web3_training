from web3 import HTTPProvider
from web3 import Web3
from web3.middleware import geth_poa_middleware
import time
import json

provider_url = "https://bsc-dataseed4.binance.org/" # rpc link
web3 = Web3(HTTPProvider(provider_url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
latestBlocknumber = web3.eth.blockNumber

with open("abi/erc_20.json", "r") as f:
    abi = json.loads(f.read())  
address = "0x7083609fCE4d1d8Dc0C979AAb8c869Ea2C873402"
contract = web3.eth.contract(abi=abi, address=address)


#câu a
events = contract.events.Transfer.createFilter(fromBlock=latestBlocknumber-999, toBlock=latestBlocknumber).get_all_entries()
event_list = []
for event in events:
    event_list.append(json.loads(web3.toJSON(event)))

data_dict = {
    "blocksInfo": {
    "startBlock": latestBlocknumber-999,
    "endBlock": latestBlocknumber
  },
  "transferEvents": event_list
}
data = json.dumps(data_dict)
with open('ex2a.json', 'w') as file1:
  file1.write(data)
file1.close()

#câu b
decimal = contract.functions.decimals().call()
data_dict_2 = {
    "decimal": decimal
}
data_2 = json.dumps(data_dict_2)
with open('ex2b.json', 'w') as file2:
  file2.write(data_2)
file2.close()

#câu c
totalSupply = contract.functions.totalSupply().call()
data_dict_3 = {
    "totalSupply": totalSupply
}
data_3 = json.dumps(data_dict_3)
with open('ex2c.json', 'w') as file3:
  file3.write(data_3)
file3.close()

#câu d
thisdict = {}
for i in range(len(event_list)):
  thisdict[event_list[i]["args"]["from"]] = 0

for i in range(len(event_list)):
  thisdict[event_list[i]["args"]["from"]] += 1

max = 0
wallet = ''
for x,y in thisdict.items():
    if y > max:
        max = y
        wallet = x

balance = contract.functions.balanceOf(wallet).call()
data_dict_4 = {
    "blocksInfo": {
    "startBlock": latestBlocknumber-999,
    "endBlock": latestBlocknumber
  },
  "wallet": wallet,
  "maxFrequency": max,
  "balance": balance
}
data_4 = json.dumps(data_dict_4)
with open('ex2d.json', 'w') as file4:
  file4.write(data_4)
file4.close()


#câu e
thisdict = {}
for i in range(len(event_list)):
  thisdict[event_list[i]["args"]["to"]] = 0

for i in range(len(event_list)):
  thisdict[event_list[i]["args"]["to"]] += 1

max = 0
wallet = ''
for x,y in thisdict.items():
    if y > max:
        max = y
        wallet = x

balance = contract.functions.balanceOf(wallet).call()
data_dict_5 = {
    "blocksInfo": {
    "startBlock": latestBlocknumber-999,
    "endBlock": latestBlocknumber
  },
  "wallet": wallet,
  "maxFrequency": max,
  "balance": balance
}
data_5 = json.dumps(data_dict_5)
with open('ex2e.json', 'w') as file5:
  file5.write(data_5)
file5.close()


#câu f
symbol = contract.functions.symbol().call()
name = contract.functions.name().call()
data_dict_6 = {
  "symbol": symbol,
  "name": name
}
data_6 = json.dumps(data_dict_6)
with open('ex2f.json', 'w') as file6:
  file6.write(data_6)
file6.close()
