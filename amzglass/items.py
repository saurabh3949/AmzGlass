# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmzProduct(scrapy.Item):
    html_file = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    brand = scrapy.Field()
    feature_bullets = scrapy.Field()
    description = scrapy.Field()
    details = scrapy.Field()
    tech_specs = scrapy.Field()

