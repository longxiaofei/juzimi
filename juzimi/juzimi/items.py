# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JuzimiItem(scrapy.Item):
	author = scrapy.Field()
	post_title = scrapy.Field()
	post_content = scrapy.Field()
	post_url = scrapy.Field()