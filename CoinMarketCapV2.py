# -*- coding: utf-8 -*-
"""
Created on Fri May  4 09:58:35 2018

@author: john
"""

import json 
import requests
import numpy as np
import pandas as pd 
import csv

# import the list of coins you want to look at
with open('coinList.csv', 'r') as f:
  reader = csv.reader(f)
  coinList = np.asarray(list(reader))   # convert to numy array

coinList = np.delete(coinList, 0, 0)    # delete header
coinList = coinList[:, :2]

# append empty columns
z = np.zeros((len(coinList),2))             # market cap | price
coinList = np.append(coinList, z, axis=1)

z = np.zeros((len(coinList),1))
coinList = np.append(z, coinList, axis=1)   # rank

# print(coinList)
#%%

# for each site of coinMarketcap request info
# https://api.coinmarketcap.com/v2/ticker/?start=1&limit=100

for k in range(17):
    
    url = 'https://api.coinmarketcap.com/v2/ticker/?start='+str(100*k+1)+'&limit=100'
    r = requests.get(url)
    buffer = r.json()
    data = buffer['data']

    if data != None:         # only if response was ok
        for item in data:               
            coin = data[item]
            for i in range(len(coinList)):
                if coin["name"] == coinList[i][2]:
                    coinList[i][0] = coin["rank"]
                    coinList[i][3] = coin['quotes']['USD']['market_cap']
                    coinList[i][4] = coin['quotes']['USD']['price']
            
                elif coin["symbol"] == coinList[i][1]:
                    coinList[i][0] = coin["rank"]
                    coinList[i][3] = coin['quotes']['USD']['market_cap']
                    coinList[i][4] = coin['quotes']['USD']['price']

print(coinList)

# save to csv
df = pd.DataFrame(coinList)
df.to_csv("results.csv")
