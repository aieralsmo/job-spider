# -*- coding: utf-8 -*-
import scrapy
import re
import os
import chardet
from furl import furl 
from tinydb import TinyDB, Query
import json
from chardet import detect 
from scrapy import Selector
from Jobs.items import Job51Item

class Job51spiderSpider(scrapy.Spider):
    name = 'job51spider'
    allowed_domains = ['www.51job.com', 'search.51job.com']
    cache_db = TinyDB('51jobSpider-cache.json')  # 缓存数据库

    start_urls = ['https://www.51job.com/']
    base_url = 'https://search.51job.com/list/{0},000000,0000,00,9,99,{1},2,1.html'
    init_city_code_url = 'https://js.51jobcdn.com/in/js/2016/layer/area_array_c.js?20180319'
    def parse_init_city_code(self, response):

        encoding = chardet.detect(response.body)['encoding']
        resp_text = response.body.decode(encoding, 'ignore')
        js_text = re.search(r'.*?=(.*?);',resp_text, re.S)
        js_text = js_text.group(1)
        js_dict = json.loads(js_text)

        city_info = {}
        for v in js_dict:
            city_info.update({'name':js_dict[v],'code':v})
            self.cache_db.insert(city_info)
            
    def start_requests(self):
        if not bool(self.cache_db.all()):
            yield scrapy.Request(url=self.init_city_code_url, callback=self.parse_init_city_code)
        
        url_params = {
            'lang': 'c',
            'postchannel': 0000,
            'workyear': 99,
            'cotype': 99,
            'degreefrom': 99,
            'jobterm': 99,
            'companysize': 99,
            'radius': -1,
            'lonlat':'0,0',
            'ord_field': 0,
            'confirmdate':9,
            'dibiaoid': 0,
            'address': None,
            'specialarea': 00,
            
                    }

        Q = Query()
        city = input("工作城市：")
        kw = input("工作职位：")
        # import ipdb; ipdb.set_trace()
      
        city_code="000000"
        city = self.cache_db.get(Q.name.search(city))
        if isinstance(city, dict):
            if city:
                city_code = city["code"]
       

        base_url = self.base_url.format(city_code, kw)
        F = furl(base_url)
        full_url = F.copy().add(url_params).url
        yield scrapy.Request(url=full_url,callback=self.parse)


    def parse(self, response):

        selector = Selector(text=response.text)

        els = selector.xpath('//div[@id="resultList"]/div[@class="el"]')
        now_page_num = response.css("div.p_in ul li.on::text").extract_first()
        print("正在爬取第{0}页\n".format(now_page_num).center(50,'*'))
        item = Job51Item()
        for el in els:

            item['job'] = el.css('p.t1 span a::attr(title)').extract_first()
            item['url'] = el.css('p.t1 span a::attr(href)').extract_first()
            item['company'] = el.css('span.t2 a::attr(title)').extract_first()
            item['address'] = el.css('span.t3::text').extract_first()            
            item['salary'] = el.css('span.t4::text').extract_first()            
            item['publish_date'] = el.css('span.t5::text').extract_first()           

            yield item

        dw_page_url = response.css("div.p_in ul li.bk:last-child > a::attr(href)").extract_first()
        if dw_page_url:
            yield scrapy.Request(url=dw_page_url,callback=self.parse)
