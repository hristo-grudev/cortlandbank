import scrapy

from scrapy.loader import ItemLoader

from ..items import CortlandbankItem
from itemloaders.processors import TakeFirst


class CortlandbankSpider(scrapy.Spider):
	name = 'cortlandbank'
	start_urls = ['https://www.cortlandbank.com/company/blog']

	def parse(self, response):
		post_links = response.xpath('//a[@class="sfpostFullStory sffullstory red-btn"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//div[@class="sf_pagerNumeric"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h2[@class="sfpostTitle sftitle"]/text()').get()
		description = response.xpath('//div[@class="sfpostContent sfcontent"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="sfpostAuthorAndDate sfmetainfo"]/text()').get()

		item = ItemLoader(item=CortlandbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
