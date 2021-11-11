from typing import Text
from numpy.core.fromnumeric import sort
import pandas as pd
import matplotlib.pyplot as plt
import json
import numpy as np

df = pd.read_csv('result.csv',dtype='unicode')
df.query('status == "CŨ"',inplace = True)
df['price'] = pd.to_numeric(df['price'],downcast='float')
result = ''

def run():
    print('1. Xem tất cả')
    print('2. Xem theo brand')
    print('3. Xem theo model')
    print('4. Exit()')
    key = input('Chon: ')
    app(key)

def app(key):
    
    def getCarByMfg():
        global result
        mfg = input("MFG: ")
        print(result.query('mfg == "'+mfg+'"') )
        return run()

    def getCarByBrand():
        # pd.set_option('max_rows',None)
        print(sort(df['name'].unique().tolist()))
        brand = input('Nhap brand: ')
        result = df.groupby(['name'])
        print(result.get_group(brand))
        return run()

    def getCarByCarmodel():
        global result
        pd.set_option('display.max_rows', None)
        model = input('Nhap model: ')
        result = df[df['carmodel'] == model]
        print(result)
        print("1. Thong ke theo nam")
        key = input('Nhap key: ')
        switcher = {
            1:getCarByMfg,
        }
        
        func = switcher.get(int(key),"Khong hop le")
        return func()

    switcher = {
        1:lambda:print(df),
        2:getCarByBrand,
        3:getCarByCarmodel,
    }
    func = switcher.get(int(key),"Khong hop le")
    return func()

run()