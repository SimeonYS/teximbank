import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import TeximbankItem
from itemloaders.processors import TakeFirst
pattern = r'(\xa0)?'

class TeximbankSpider(scrapy.Spider):
	name = 'teximbank'
	start_urls = ['https://www.teximbank.bg/all/novini']


	def parse(self, response):
		yield response.follow(response.url, self.parse_articles, dont_filter=True)

		next_page = response.xpath('//a[@class="more_news"][last()]/@href').get()
		if next_page:
			yield response.follow(next_page, self.parse)

	def parse_articles(self, response):

		date = response.xpath('//div[@class="news-date"]')
		length = len(date)

		for index in range(length):
			item = ItemLoader(item=TeximbankItem(), response=response)
			item.default_output_processor = TakeFirst()

			date = response.xpath(f'(//div[@class="news-date"])[{index+1}]/text()').get()
			title = response.xpath(f'(//h2)[{index+1}]/text()').get()
			content = response.xpath(f'(//div[@class="news-text"])[{index+1}]//text()').getall()
			content = [p.strip() for p in content if p.strip()]
			content = re.sub(pattern, "", ' '.join(content))

			item.add_value('title', title)
			item.add_value('link', response.url)
			item.add_value('content', content)
			item.add_value('date', date)

			yield item.load_item()