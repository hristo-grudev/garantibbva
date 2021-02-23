import scrapy

from scrapy.loader import ItemLoader
from ..items import GarantibbvaItem
from itemloaders.processors import TakeFirst


class GarantibbvaSpider(scrapy.Spider):
	name = 'garantibbva'
	start_urls = ['https://www.garantibbva.com.tr/en/our_company/garanti_news.page']

	def parse(self, response):
		post_links = response.xpath('//div[@class="promoBase promoBoxSilver"]//a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//div[@class="contentBox"]/h2//text()').get()
		description = response.xpath('//div[@class="contentBox"]//text()[normalize-space() and not(ancestor::h2)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=GarantibbvaItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)

		return item.load_item()
