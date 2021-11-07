from typing import Text
from numpy.core.fromnumeric import sort
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
def priceFilter(carmodel,price):
    car = {
        '3':  700000000,
        'LUX A 2.0':700000000,
        'RUSH': 500000000
    }
    if carmodel in car:
        if car[carmodel] >= float(price):
            return True
        else:
            return False

if(priceFilter('3',7000000000) != True):
    print('oke')
else:
    print('not oke')
# df = pd.read_csv('result.csv',dtype='unicode')
# df['price'] = pd.to_numeric(df['price'],downcast='float')
# df=df[df['price']>350000000]
# value = df.groupby(['name','carmodel']).mean()['price']
# # value = value[value>700000000]
# # print(df)
# # performance = np.array(value).tolist()
# # car = sort(df['carmodel'].unique().tolist())
# y_pos = np.arange(len(value))
# value.plot.barh()
# plt.show()


