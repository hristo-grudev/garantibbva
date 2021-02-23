import scrapy


class GarantibbvaItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
