from typing import Text
from numpy.core.fromnumeric import sort
import pandas as pd
import matplotlib.pyplot as plt
import json
import numpy as np
import plotext as plx


df = pd.read_csv('D:/vucar/scraper/scraper/spiders/result.csv',dtype='unicode')
df.query('status == "CŨ"',inplace = True)
df['price'] = pd.to_numeric(df['price'],downcast='float')
result = ''
brand=''
model=''

def run():
    print('1. Xem tất cả')
    print('2. Xem theo brand')
    print('3. Exit()')
    key = input('Chon: ')
    app(key)

def app(key):
    def getPrice():
        global result,brand,model
        years = result['mfg'].unique().tolist()
        prices = result.groupby(['mfg']).mean()['price'].tolist()
        # y_pos =  np.arange(len(years))
        years.sort()
        # plt.bar(y_pos,prices)
        # plt.xticks(y_pos,years)
        # value = result.groupby(['mfg']).mean()['price']
        # value.plot.bar()
        # plt.title((brand,model))
        # plt.grid()
        # plt.show()
        # print(prices)
        # print(result['mfg'].unique().tolist())
        plx.bar(years,prices)
        # plx.title((brand,model))
        plx.show()
        return 0
    def getCarByMfg():
        pd.set_option('max_columns',None)
        pd.set_option('max_colwidth', None)
        global result
        mfg = input("MFG: ")
        print(result.query('mfg == "'+mfg+'"') )
        return run()

    def getCarByBrand():
        global result,brand,model
        # pd.set_option('max_rows',None)
        print(sort(df['name'].unique().tolist()))
        brand = input('Nhap brand: ')
        result = df.groupby(['name']).get_group(brand)
        print(result)
        print("1. Xem theo model")
        print("2. quay ve")
        key = input('Nhap key: ')
        switcher = {
            1:getCarByCarmodel,
            2:run,
        }
        
        func = switcher.get(int(key),"Khong hop le")
        return func()

    def getCarByCarmodel():
        global result,brand,model
        pd.set_option('display.max_rows', None)
        model = input('Nhap model: ')
        # result = df[df['carmodel'] == model]
        result = result.query('carmodel == "'+model+'"')
        print(result)
        print("1. Xem xe theo nam")
        print("2. Thong ke theo cac nam")
        print("3. quay ve")
        key = input('Nhap key: ')
        switcher = {
            1:getCarByMfg,
            2:getPrice,
            3:run,
        }
        
        func = switcher.get(int(key),"Khong hop le")
        return func()

    switcher = {
        1:lambda:print(df),
        2:getCarByBrand,
        3:exit,
    }
    func = switcher.get(int(key),"Khong hop le")
    return func()

run()