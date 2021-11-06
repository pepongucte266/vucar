from typing import Text
import scrapy
from scrapy.crawler import CrawlerProcess
from ..items import ScraperItem
import jsonlines
from numpy.core.fromnumeric import sort
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
class Carbonbanh(scrapy.Spider):

    name = 'carbonbanhhh'
    start_urls = [
        'https://bonbanh.com/oto/page,%d' % i for i in range(1,2) 
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
        yield items


class Car(scrapy.Spider):
    name = 'car'
    start_urls = [
        'https://www.carmudi.vn/mua-ban-o-to/index%d.html' % i for i in range(1,2) 
    ] 
    def parse(self,response):
        for link in response.xpath('//*[@id="listings"]/article/div/div/div/div/a/@href').getall():
            yield scrapy.Request(response.urljoin(link),self.parse_carmudi)

    def parse_carmudi(self,response):
        items = ScraperItem()
        
        items['name'] = response.xpath('//*[@id="controller_area"]/div[1]/div[1]/div[4]/div[1]/span/text()').extract()[0].strip().upper()
        items['carmodel'] = response.xpath('//*[@id="controller_area"]/div[1]/div[1]/div[4]/div[2]/span/text()').extract()[0].strip().upper()
        items['price'] = response.xpath('//*[@id="controller_area"]/div[1]/div[1]/div[3]/div[2]/@data-price').get().replace(".","")
        items['location'] = response.xpath('//*[@id="controller_area"]/div[1]/div[1]/div[4]/div[7]').get().split('\n')[2].split(':')[1].strip().upper()
        items['status'] = response.xpath('//*[@id="controller_area"]/div[1]/div[1]/div[4]/div[5]').get().split('\n')[2].split(':')[1].strip().upper()
        items['mfg'] = response.xpath('//*[@id="controller_area"]/div[1]/div[1]/div[4]/div[4]').get().split('\n')[2].split(':')[1].strip().upper()
        items['interiorColor'] = ''
        items['exteriorColor'] = response.xpath('//*[@id="controller_area"]/div[1]/div[1]/div[4]/div[11]').get().split('\n')[2].split(':')[1].strip().upper()
        items['gearbox'] = response.xpath('//*[@id="controller_area"]/div[1]/div[1]/div[4]/div[6]').get().split('\n')[2].split(':')[1].strip().upper()
        items['kilometer'] = '0'
        items['link'] = response.url

        yield items

class Carchotot(scrapy.Spider):
    name = 'carchotot'
    start_urls = [
        'https://xe.chotot.com/mua-ban-oto?page=%d' % i for i in range(1,2) 
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
with jsonlines.open('D:/vucar/scraper/result.jl') as reader:
    for obj in reader:
        data.append(obj)
reader.close()

result = pd.DataFrame(data)
result.to_csv('result.csv',index= None,encoding='utf-8-sig')


df = pd.read_csv('result.csv',dtype='unicode')
df['price'] = pd.to_numeric(df['price'],downcast='float')
value = df.groupby('carmodel').mean()['price']
performance = np.array(value).tolist()
car = sort(df['carmodel'].unique()).tolist()
y_pos = np.arange(len(car))
# print(np.array(value).tolist())

plt.barh(y_pos, performance)
plt.yticks(y_pos,car)
plt.xlabel('price')
plt.ylabel('gia tien trung binh tung dong xe')
plt.savefig('ave.png')