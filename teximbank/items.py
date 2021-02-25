import scrapy


class TeximbankItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    date = scrapy.Field()
    link = scrapy.Field()
