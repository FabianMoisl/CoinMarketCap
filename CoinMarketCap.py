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

coinList = np.delete(coinList, 0, 0)
coinList = coinList[:, :3]

# append empty columns
z = np.zeros((len(coinList),2))
coinList = np.append(coinList, z, axis=1)

#%%

# for each site of coinMarketcap request info
for k in range(17):
    
    url = 'https://api.coinmarketcap.com/v1/ticker/?start='+str(100*k+1)+'&limit=100'
    r = requests.get(url)

    for coin in r.json():
        if coin != 'error':                 # only if response was ok
            for i in range(len(coinList)):
                if coin["name"] == coinList[i][2]:
                    coinList[i][4] = coin["price_usd"]
                    coinList[i][3] = coin["market_cap_usd"]
                    coinList[i][0] = coin["rank"]
            
                elif coin["symbol"] == coinList[i][1]:
                    coinList[i][4] = coin["price_usd"]
                    coinList[i][3] = coin["market_cap_usd"]
                    coinList[i][0] = coin["rank"]

print(coinList)

# save to csv
df = pd.DataFrame(coinList)
df.to_csv("results.csv")
