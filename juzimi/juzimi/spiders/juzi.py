# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from juzimi.items import *
from urllib import parse
from copy import deepcopy
from pyquery import PyQuery as pq

class JuziSpider(Spider):
    name = 'juzi'
    allowed_domains = ['www.juzimi.com']
    start_urls = ['http://www.juzimi.com/dynasty/近现代']
    head_url = 'http://www.juzimi.com'

    def parse(self, response):
    	author_list = response.css('#block-views-xqtermspagewriterage-block_1 .view-content .views-field-name a')
    	for author in author_list:
            author_name = author.css('::text').extract_first()
            author_detail_url = parse.urljoin(self.head_url, author.css('::attr(href)').extract_first())
            yield Request(url=author_detail_url, meta=deepcopy({'author': author_name}), callback=self.parse_detail)

    	next_url = parse.urljoin(self.head_url, response.css('.item-list .pager-next a::attr(href)').extract_first())
    	yield Request(url=next_url, callback=self.parse)
    
    def parse_detail(self, response):
    	doc = pq(response.text)
    	post_list = doc('#block-views-xqfamoustermspage-block_1 .view-content .views-row').items()
    	for post in post_list:
    		item = JuzimiItem()
    		post_content = post.find('.views-field-phpcode-1').text()
    		post_title = post.find('.xqjulistwafo span a').text().strip('（全文）')
    		post_url = post.find('.views-field-phpcode-1 a').attr('href')
    		post_data = {
    			'post_url': post_url,
    			'post_title': post_title,
    			'post_content': post_content,
    			'author': response.meta['author'],
    		}
    		for field in item.fields:
    			if field in post_data.keys():
    				item[field] = post_data.get(field)
    		yield item

    	next_url = parse.urljoin(self.head_url, response.css('#block-views-xqfamoustermspage-block_1 .item-list .pager-next a::attr(href)').extract_first())
    	yield Request(url=next_url, meta=deepcopy(response.meta), callback=self.parse_detail)

        
