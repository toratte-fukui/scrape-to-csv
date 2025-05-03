# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperItem(scrapy.Item):
    title = scrapy.Field()
    start_price = scrapy.Field()
    end_price = scrapy.Field()
    bid_num = scrapy.Field()
    start_datetime = scrapy.Field()
    end_datetime = scrapy.Field()
    url = scrapy.Field()
    image_url = scrapy.Field()
    image_url2 = scrapy.Field()
    image_url3 = scrapy.Field()
