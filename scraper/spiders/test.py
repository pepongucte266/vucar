from datetime import datetime
from typing import Text
from numpy.core.fromnumeric import sort
import pandas as pd
import matplotlib.pyplot as plt
import json
import numpy as np
from datetime import date
import yagmail


# def rollup2(x):
#     return x.set_index('mfg')['price'].to_dict()
# def rollup3(x):
#     return x.groupby('carmodel').apply(rollup2).to_dict()
# def createNewFilterFile():
#     pd.set_option('display.max_rows', None)
#     df = pd.read_csv('currentData.csv',dtype='unicode')
#     df['price'] = pd.to_numeric(df['price'],downcast='float')
#     cars = df[['name','mfg','carmodel','price']].sort_values('name').groupby(['name','carmodel','mfg']).mean().reset_index(level='carmodel').reset_index(level='mfg')
#     cars.groupby(['name']).apply(rollup3).to_json('test.json', orient='index', force_ascii=False)

# def extendData(curentData,oldData,todayData):
#     n = todayData[~todayData.isin(curentData)].dropna(how='all')
#     curentData = pd.concat([curentData,n])
#     curentData = curentData.drop_duplicates()
#     curentData = pd.concat([curentData,oldData]).drop_duplicates(keep=False)
#     curentData = curentData[~curentData.isin(oldData)].dropna(how='all')
#     n.to_csv('oldData.csv',index= None,encoding='utf-8-sig')
#     return curentData

# curentData = pd.read_csv('currentData.csv',dtype='unicode')
# todayData = pd.read_csv('[DAILY DATA] 2021-11-25 result.csv',dtype='unicode')
# oldData = pd.read_csv('oldData.csv',dtype='unicode')
# extendData(curentData,oldData,todayData).to_csv('currentData.csv',index= None,encoding='utf-8-sig')
# createNewFilterFile()