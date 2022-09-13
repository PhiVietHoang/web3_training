from tkinter import N
from web3 import HTTPProvider
from web3 import Web3
from web3.middleware import geth_poa_middleware
from receipt_log_handler import EthReceiptLogHandler
import time
import json

provider_url = "https://bsc-dataseed4.binance.org/" # rpc link
web3 = Web3(HTTPProvider(provider_url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
latestBlocknumber = web3.eth.blockNumber

with open("abi/masterchef_abi.json", "r") as f:
    abi = json.loads(f.read())  
address = "0xa5f8C5Dbd5F286960b9d90548680aE5ebFf07652"
contract = web3.eth.contract(abi=abi, address=address)
pid = 3

#cau 1
poolInfo = contract.functions.poolInfo(pid).call()

data_dict_1 = {
    "poolInfo":{
        "accCakePerShare": poolInfo[0],
        "lastRewardBlock": poolInfo[1],
        "allocPoint": poolInfo[2],
        "totalBoostedShare": poolInfo[3],
        "isRegular": poolInfo[4]
    }
}
data_1 = json.dumps(data_dict_1)
with open('uniswap1.json', 'w') as file1:
  file1.write(data_1)
file1.close()

#cau 2
addressLpToken = contract.functions.lpToken(pid).call()
data_dict_2 = {
    "lpTokenAddress": addressLpToken
}
data_2 = json.dumps(data_dict_2)
with open('uniswap2.json', 'w') as file2:
  file2.write(data_2)
file2.close()

#cau 3
with open("abi/lp_token_abi.json", "r") as f:
    abiLpToken = json.loads(f.read())  

contractLpToken = web3.eth.contract(abi=abiLpToken, address=addressLpToken)
token0 = contractLpToken.functions.token0().call()
token1 = contractLpToken.functions.token1().call()
reserves = contractLpToken.functions.getReserves().call()
data_dict_3 = {
    token0: reserves[0],
    token1: reserves[1]
}
data_3 = json.dumps(data_dict_3)
with open('uniswap3.json', 'w') as file3:
  file3.write(data_3)
file3.close()


#cau 4
with open("abi/lp_token_abi.json", "r") as f:
    event_abi = json.loads(f.read())

handler = EthReceiptLogHandler()
event_abi_info = handler.build_list_info_event(event_abi)

event_hash = [event_info[1] for event_info in event_abi_info]

event_subscriber = {}
for info in event_abi_info:
    event_subscriber[info[1]] = info[0]

filter_params = {
    "fromBlock":latestBlocknumber-999,
    "toBlock":latestBlocknumber,
    "topics": [event_hash],
    "address":[addressLpToken]
}

event_filter = web3.eth.filter(filter_params)
event_logs = event_filter.get_all_entries()
event_list = []
for event_log in event_logs:
    log = handler.web3_dict_to_receipt_log(event_log)
    eth_event = handler.extract_event_from_log(log, event_subscriber[log.topics[0]])
    if eth_event is not None:
        eth_event_dict = handler.eth_event_to_dict(eth_event)
        event_list.append(eth_event_dict)
web3.eth.uninstallFilter(event_filter.filter_id)

data_4 = json.dumps(event_list)
with open('uniswap4.json', 'w') as file4:
  file4.write(data_4)
file4.close()


#cau 5
trans = contractLpToken.events.Transfer.createFilter(fromBlock=latestBlocknumber-999, toBlock=latestBlocknumber).get_all_entries()
event_list_trans = []
for event in trans:
    event_list_trans.append(json.loads(web3.toJSON(event)))

data_dict_5 = {
  "transferEvents": event_list_trans
}
data = json.dumps(data_dict_5)
with open('uniswap5.json', 'w') as file5:
  file5.write(data)
file5.close()



#cau 6
thisdict = {}
for i in range(len(event_list_trans)):
  thisdict[event_list_trans[i]["args"]["from"]] = 0

for i in range(len(event_list_trans)):
  thisdict[event_list_trans[i]["args"]["from"]] += 1

max = 0
wallet = ''
for x,y in thisdict.items():
    if y > max:
        max = y
        wallet = x

data_dict_6 = {
    "blocksInfo": {
    "startBlock": latestBlocknumber-999,
    "endBlock": latestBlocknumber
  },
  "maxFrequency": max,
  "wallet": wallet,
}
data_6 = json.dumps(data_dict_6)
with open('uniswap6.json', 'w') as file6:
  file6.write(data_6)
file6.close()


#cau 7
user = contract.functions.userInfo(256,wallet).call() 
data_dict_7 = {
    "amount": user[0],
    "rewardDebt": user[1]
}
data_7 = json.dumps(data_dict_7)
with open('uniswap7.json', 'w') as file7:
  file7.write(data_7)
file7.close()