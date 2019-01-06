# -*- coding: utf-8 -*-
import scrapy

from Jobs.items import HuiboItem

class HuibospiderSpider(scrapy.Spider):
	name = 'huibospider'
	allowed_domains = ['www.huibo.com']
	start_urls = ['http://www.huibo.com/']


	def start_requests(self):
		kw = input("职位名称：")
		base_url = 'http://www.huibo.com/jobsearch/?key={0}'.format(kw)
		yield scrapy.Request(url=base_url, callback=self.parse)


	def parse(self, response):

		postIntros = response.css("div#job_list_table div.postIntro")

		for postIntro in postIntros:

			item = HuiboItem()
			try:

				item['company'] = postIntro.css('div.title> a::attr(title)').extract_first().strip()
				item['url'] = postIntro.css("div.postIntroList span.name a::attr(href)").extract_first().strip()
				item['job'] = postIntro.css("div.postIntroList span.name a::text").extract()[-1].strip()
				item['salary'] = postIntro.css("div.postIntroList span.money::text").extract_first().strip()
				item['address'] = postIntro.css("div.postIntroList span.address::text").extract_first().strip()
				item['exp'] = postIntro.css("div.postIntroList span.exp::text").extract_first().strip()
				print(item["job"])
				yield item
			except Exception as e:
				print(e)


		next_page_url = response.css('div.page a:last-child::attr(href)').extract_first("")
		if next_page_url.startswith("http://"):
			print('next_page_url',next_page_url)
			yield scrapy.Request(url=next_page_url, callback=self.parse)

