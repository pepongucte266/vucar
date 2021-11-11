# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    carmodel = scrapy.Field()
    link = scrapy.Field()
    location = scrapy.Field()
    price = scrapy.Field()
    status = scrapy.Field()
    mfg = scrapy.Field()
    interiorColor = scrapy.Field()
    exteriorColor = scrapy.Field()
    gearbox = scrapy.Field()
    kilometer = scrapy.Field()
    note = scrapy.Field()
    
