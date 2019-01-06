# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Job51Item(scrapy.Item):

    job = scrapy.Field()
    url = scrapy.Field()
    company = scrapy.Field()
    address = scrapy.Field()
    salary = scrapy.Field()
    publish_date = scrapy.Field()



class ZhaopinItem(scrapy.Item):

    job = scrapy.Field()
    url = scrapy.Field()
    company = scrapy.Field()
    address = scrapy.Field()
    salary = scrapy.Field()
    publish_date = scrapy.Field()
    eduLevel = scrapy.Field()
    workingExp = scrapy.Field()
    positionURL = scrapy.Field()


class HuiboItem(scrapy.Item):
    company = scrapy.Field()
    url = scrapy.Field()
    job = scrapy.Field()
    salary = scrapy.Field()
    address = scrapy.Field()
    exp = scrapy.Field()

            