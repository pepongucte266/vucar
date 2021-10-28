from typing import Text
import scrapy

class Car(scrapy.Spider):
    name = 'car'
    allowed_domains = ['carmudi.vn']
    
    def start_requests(self):
        urls = [
            'https://www.carmudi.vn/mua-ban-o-to/index1.html',
            'https://www.carmudi.vn/mua-ban-o-to/index2.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)

    def parse_item(self,response):
        carinfo = {}
        carinfo['link'] = response.url
        carinfo['name'] = response.xpath('//*[@id="controller_area"]/div[1]/div[1]/div[4]/div[1]/span/text()').extract()[0].strip().upper()
        carinfo['carmodel'] = response.xpath('//*[@id="controller_area"]/div[1]/div[1]/div[4]/div[2]/span/text()').extract()[0].strip().upper()
        carinfo['price'] = response.xpath('//*[@id="controller_area"]/div[1]/div[1]/div[3]/div[2]/@data-price').get().replace(".","")
        # for key, text in carinfo.items():
        #     infor ="{key} : {text}".format(key=key.upper(), text=text)
        #     print (infor)
        yield carinfo

    
    def parse(self,response):
        
        for link in response.xpath('//*[@id="listings"]/article/div/div/div/div[1]/a/@href').getall():
            
            yield scrapy.Request(response.urljoin(link),self.parse_item)
