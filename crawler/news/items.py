import scrapy


class NewsItem(scrapy.Item):

    id = scrapy.Field()
    language = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    timestamp = scrapy.Field()
    date = scrapy.Field()
    agency = scrapy.Field()
    author = scrapy.Field()
    category = scrapy.Field()
    image_url = scrapy.Field()
    image_alt = scrapy.Field()
    paragraphs = scrapy.Field(serializer=list)
