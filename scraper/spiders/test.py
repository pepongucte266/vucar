from datetime import datetime
from typing import Text
from numpy.core.fromnumeric import sort
import pandas as pd
import matplotlib.pyplot as plt
import json
import numpy as np
from datetime import date
import yagmail


# pd.set_option('display.max_rows', None)
# df = pd.read_csv('result.csv',dtype='unicode')
# df['price'] = pd.to_numeric(df['price'],downcast='float')

# cars = df[['name','mfg','carmodel','price']].sort_values('name').groupby(['name','carmodel','mfg']).mean().reset_index(level='carmodel').reset_index(level='mfg')

# # cars.groupby(['name']).apply(lambda x: x.set_index('carmodel')['price'].to_dict()).to_json('test.json', orient='index', force_ascii=False)


# def rollup2(x):
#     return x.set_index('mfg')['price'].to_dict()
# def rollup3(x):
#     return x.groupby('carmodel').apply(rollup2).to_dict()

# data = cars.groupby(['name']).apply(rollup3).to_json('test.json', orient='index', force_ascii=False)
# def filterCar(item):
#     result =''
#     with open(r'D:\vucar\scraper\scraper\spiders\test.json',encoding = 'utf-8') as filterfile:
#         data = json.load(filterfile)
#         if(item['name'] not in data.keys()):
#             result += 'brand not in list'
#         elif(item['carmodel'] not in data[item['name']].keys()):
#             result += "model not in brand"
#         elif(item['mfg'] not in data[item['name']][item['carmodel']].keys()):
#             result += "mfg not in list"
#         elif(float(item['price'])/data[item['name']][item['carmodel']][item['mfg']]*100 > 150 or float(item['price'])/data[item['name']][item['carmodel']][item['mfg']]*100 < 60 ):
#             result += 'price!!!'
#     return result

# item = {}
# item['carmodel'] = 'Q7'
# item['name'] = 'AUDI'
# item['mfg'] = '12'
# item['price'] = '2500000000'
# # print(item['name'])
# print(filterCar(item))
# # filterCar(item)