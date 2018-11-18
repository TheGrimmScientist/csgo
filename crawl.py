# -*- coding: utf-8 -*-
import scrapy


class CrawlSpider(scrapy.Spider):
    name = 'crawl'
    allowed_domains = ['cs_spider']
    start_urls = ['http://cs_spider/']

    def parse(self, response):
        pass
