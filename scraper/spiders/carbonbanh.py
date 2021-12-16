# -*- coding: utf-8 -*- 
from datetime import datetime
from typing import Text
import scrapy
from scrapy.crawler import CrawlerProcess
from ..items import ScraperItem
import jsonlines
from numpy.core.fromnumeric import sort
import pandas as pd
import numpy as np
import yagmail
import json
from datetime import date
import os


if os.path.isfile('result.jl'):
    os.remove('result.jl')
if os.path.isfile('warning.csv'):
    os.remove('warning.csv')

def rollup2(x):
    return x.set_index('mfg')['price'].to_dict()
def rollup3(x):
    return x.groupby('carmodel').apply(rollup2).to_dict()
def createNewFilterFile():
    pd.set_option('display.max_rows', None)
    df = pd.read_csv('currentData.csv',dtype='unicode')
    df['price'] = pd.to_numeric(df['price'],downcast='float')
    df = df.query('note != "price!!!"')
    cars = df[['name','mfg','carmodel','price']].sort_values('name').groupby(['name','carmodel','mfg']).mean().reset_index(level='carmodel').reset_index(level='mfg')
    cars.groupby(['name']).apply(rollup3).to_json('test.json', orient='index', force_ascii=False)

def extendData(curentData,oldData,todayData):
    n = todayData[~todayData.isin(curentData)].dropna(how='all')
    curentData = pd.concat([curentData,n])
    curentData = curentData.drop_duplicates()
    curentData = pd.concat([curentData,oldData]).drop_duplicates(keep=False)
    curentData = curentData[~curentData.isin(oldData)].dropna(how='all')
    n.to_csv('oldData.csv',index= None,encoding='utf-8-sig')
    curentData = curentData.drop_duplicates(subset=['link'])
    return curentData

def filterCar(item):
    result =''
    with open('test.json',encoding = 'utf-8') as filterfile:
        data = json.load(filterfile)
        if(item['name'] not in data.keys()):
            result += 'brand not in list'
        elif(item['carmodel'] not in data[item['name']].keys()):
            result += "model not in brand"
        elif(item['mfg'] not in data[item['name']][item['carmodel']].keys()):
            result += "mfg not in list"
        elif(float(item['price'])/data[item['name']][item['carmodel']][item['mfg']]*100 > 125 or float(item['price'])/data[item['name']][item['carmodel']][item['mfg']]*100 < 85 ):
            result += 'price!!!'
    return result


class Carbonbanh(scrapy.Spider):

    name = 'carbonbanhhh'
    start_urls = [
        'https://bonbanh.com/oto/page,%d' % i for i in range(1,1887) 
    ] 
    def parse(self,response):
        items = ScraperItem()

        links = response.xpath('//*[@id="s-list-car"]/div/ul/li/a/@href').getall()
        prices = response.xpath('//b/@content').getall()
        locations = response.xpath('//div[@class="cb4"]/b/text()').getall()
        
        
        for i in range(1,len(links)):
            items['price'] = prices[i]
            items['location'] = locations[i].replace('TP HCM','hồ chí minh').upper()
            yield scrapy.Request(response.urljoin(links[i]),meta={
                                                                'price':items['price'],
                                                               'location': items['location']
                                                                },callback=self.parse_car)  
              

    def parse_car(self,response):
        items = ScraperItem()
        items['name'] = response.xpath('//*[@id="wrapper"]/div[2]/span[3]/a/span/strong/text()').get().strip().upper()
        items['carmodel'] = response.xpath('//*[@id="wrapper"]/div[2]/span[4]/a/span/strong/text()').get().strip().upper()
        items['price'] = response.meta['price']
        
        items['location'] = response.meta['location']
        items['status'] = response.xpath('/html/body/div[1]/div[3]/div[5]/div/div[1]/div[1]/div[2]/div[2]/span/text()').get().replace("Xe mới","MỚI").replace("Xe đã dùng","CŨ").upper()
        items['mfg'] = response.xpath('//*[@id="wrapper"]/div[2]/span[5]/a/span/strong/text()').get().upper()
        items['interiorColor'] = response.xpath('/html/body/div[1]/div[3]/div[5]/div/div[1]/div[1]/div[6]/div[2]/span/text()').get().upper()
        items['exteriorColor'] = response.xpath('/html/body/div[1]/div[3]/div[5]/div/div[1]/div[1]/div[5]/div[2]/span/text()').get().upper()
        items['gearbox'] = response.xpath('/html/body/div[1]/div[3]/div[5]/div/div[1]/div[2]/div[4]/div[2]/span/text()').get().replace("Số tự động",'tự động').upper()
        items['kilometer'] = response.xpath('/html/body/div[1]/div[3]/div[5]/div/div[1]/div[1]/div[4]/div[2]/span/text()').get().split(' ')[0].replace(',','')
        items['link'] = response.url
        items['note'] = filterCar(items)
        yield items

class Car(scrapy.Spider):
    name = 'car'
    start_urls = [
        'https://www.carmudi.vn/mua-ban-o-to/index%d.html' % i for i in range(1,347) 
    ] 
    def parse(self,response):
        for link in response.xpath('//*[@id="listings"]/article/div/div/div/div/a/@href').getall():
            yield scrapy.Request(response.urljoin(link),self.parse_carmudi)

    def parse_carmudi(self,response):
        items = ScraperItem()
        
        items['name'] = response.xpath('//*[@id="controller_area"]/div[1]/div[1]/div[4]/div[1]/span/text()').extract()[0].replace('_','').strip().upper()
        items['carmodel'] = response.xpath('//*[@id="controller_area"]/div[1]/div[1]/div[4]/div[2]/span/text()').extract()[0].replace('_',' ').strip().upper().replace('LUX-A-2-0','LUX A 2.0').replace('LUX-SA-2-0','LUX SA 2.0')
        items['price'] = response.xpath('//*[@id="controller_area"]/div[1]/div[1]/div[3]/div[2]/@data-price').get().replace(".","")
        
        
        items['location'] = response.xpath('//*[@id="controller_area"]/div[1]/div[1]/div[4]/div[7]').get().split('\n')[2].split(':')[1].strip().upper()
        items['status'] = response.xpath('//*[@id="controller_area"]/div[1]/div[1]/div[4]/div[5]').get().split('\n')[2].split(':')[1].strip().upper()
        items['mfg'] = response.xpath('//*[@id="controller_area"]/div[1]/div[1]/div[4]/div[4]').get().split('\n')[2].split(':')[1].strip().upper()
        items['interiorColor'] = ''
        items['exteriorColor'] = response.xpath('//*[@id="controller_area"]/div[1]/div[1]/div[4]/div[11]').get().split('\n')[2].split(':')[1].strip().upper()
        items['gearbox'] = response.xpath('//*[@id="controller_area"]/div[1]/div[1]/div[4]/div[6]').get().split('\n')[2].split(':')[1].strip().upper()
        items['kilometer'] = '0'
        items['link'] = response.url
        items['note'] = filterCar(items)

        yield items

class Carchotot(scrapy.Spider):
    name = 'carchotot'
    start_urls = [
        'https://xe.chotot.com/mua-ban-oto?page=%d' % i for i in range(1,1266) 
    ] 
    def parse(self,response):
        # locations = response.xpath('//div[@class="Layout_bottom__3h6pN  Layout_big__2_Ayd"]').getall()
 
        for link in response.xpath('//*[@id="__next"]/div/div/div/main/div/div/div/div/ul/div/li/a/@href').getall():

            yield scrapy.Request(response.urljoin(link),self.parse_carchotot)

    def parse_carchotot(self,response):
        items = ScraperItem()
        items['name'] = response.xpath('//span[@itemprop = "carbrand"]/text()').get().strip().upper()
        items['carmodel'] = response.xpath('//span[@itemprop = "carmodel"]/text()').get().strip().upper()
        items['price'] = response.xpath('//span[@itemprop = "price"]/text()').get().replace(".","").split(' ')[0]
        
        items['status'] = response.xpath('//span[@itemprop = "condition_ad"]/text()').get().replace("Đã sử dụng","Cũ").upper()
        items['mfg'] = response.xpath('//span[@itemprop = "mfdate"]/text()').get().upper()
        items['interiorColor'] = ''
        items['exteriorColor'] = ''
        items['gearbox'] = response.xpath('//span[@itemprop = "gearbox"]/text()').get().upper()
        items['kilometer'] = response.xpath('//span[@itemprop = "mileage_v2"]/text()').get()
        items['link'] = response.url
        items['note'] = filterCar(items)

        yield items


SETTINGS = {
    'FEED_FORMAT': 'jl',
    'FEED_URI': 'result.jl',
}
process = CrawlerProcess(SETTINGS)
process.crawl(Car)
process.crawl(Carbonbanh)
process.crawl(Carchotot)
process.start()


data=[]
with jsonlines.open('result.jl') as reader:
    for obj in reader:
        data.append(obj)
reader.close()

today =date.today()
title = '[DAILY DATA] '+ str(today)+' result.csv'
result = pd.DataFrame(data)
result.to_csv(title,index= None,encoding='utf-8-sig')

df = pd.read_csv(title,dtype='unicode')
warning = df.query('note == "price!!!" or note=="model not in brand"')
rows = len(warning.index)
warningTitle = '[DAILY WARNING] '+str(rows)+' rows '+str(today)+'.csv'
warning.to_csv(warningTitle,encoding='utf-8-sig')

# "jake.long.vu@m"
receiver = ["pepongcute123@gmail.com","jake.long.vu@vucar.net"]
body = "Hello there from VUCAR (server)"
filename = [title,warningTitle]

yag = yagmail.SMTP("son.vu@vucar.net","pykpbkqlyjwmoegm")
yag.send(
    to=receiver,
    subject='[DAILY DATA] '+str(today)+" "+str(rows),
    contents=body, 
    attachments=filename,
)

curentData = pd.read_csv('currentData.csv',dtype='unicode')
todayData = pd.read_csv(title,dtype='unicode')
oldData = pd.read_csv('oldData.csv',dtype='unicode')
extendData(curentData,oldData,todayData).to_csv('currentData.csv',index= None,encoding='utf-8-sig')
createNewFilterFile()
