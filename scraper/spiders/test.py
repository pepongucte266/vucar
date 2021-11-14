from datetime import datetime
from typing import Text
from numpy.core.fromnumeric import sort
import pandas as pd
import matplotlib.pyplot as plt
import json
import numpy as np

import yagmail

# # receiver = "pepongcute123@gmail.com"
# # body = "Hello there from Yagmail"
# # filename = r"D:\vucar\scraper\scraper\spiders\1_About-MIS.pdf"

# # yag = yagmail.SMTP("pepongcute266@gmail.com",'rybzjesjmuwatwgl')
# # yag.send(
# #     to=receiver,
# #     subject="Yagmail test with attachment",
# #     contents=body, 
# #     attachments=filename,
# # )




# pd.set_option('display.max_rows', None)
# df = pd.read_csv(r'D:\vucar\scraper\result.csv',dtype='unicode')
# df['price'] = pd.to_numeric(df['price'],downcast='float')
# value = df[['name','carmodel','price']].groupby(['name','carmodel']).mean()['price']
# print(value)
# cars = df[['name','carmodel','price']].sort_values('name').groupby(['name','carmodel']).mean().reset_index(level='carmodel')
# cars.groupby('name').apply(lambda x: x.set_index('carmodel')['price'].to_dict()).to_json('filename.json', orient='index', force_ascii=False)
# # value.to_json('filename.json', orient='index')
# # # # value = value[value>700000000]
# # # # performance = np.array(value).tolist()
# # # car = sort(df['name'].unique().tolist())
# # # carmodel = sort(df['carmodel'].unique().tolist())
# # # print(car)
# # objcar = df[['name','carmodel']].sort_values('name')
# # print(objcar)
# # result = objcar.to_json("filejson.json",orient="table",index = False)


# # value.plot.barh()
# # plt.show()


# def filterCar(item):
#     result =''
#     with open(r'D:\vucar\scraper\scraper\spiders\filename.json',encoding = 'utf-8') as filterfile:
#         data = json.load(filterfile)
#         print(data['BMW']['520I'])
#         if(item['carmodel'] not in data[item['name']]):
#             result += "model not in brand"
#         elif(float(item['price'])/data[item['name']][item['carmodel']]*100 > 150 or float(item['price'])/data[item['name']][item['carmodel']]*100 < 30 ):
#             result += 'price!!!'
#     return result 

# item = {}
# item['name'] = 'ACURA'
# item['carmodel'] = 'MDX'
# item['price'] = '9900000000.0'
# item['note'] = filterCar(item)


# print(item)
# date = datetime.now()
# receiver = ["pepongcute123@gmail.com","jake.long.vu@vucar.net"]
# body = "Hello there from VUCAR"
# filename = ['result.csv','warning.csv']

# yag = yagmail.SMTP("pepongcute266@gmail.com",'rybzjesjmuwatwgl')
# yag.send(
#     to=receiver,
#     subject=str(date),
#     contents=body, 
#     attachments=filename,
# )