# -*- coding: utf-8 -*-
import scrapy

"""
game IDs are consecutive, https://play.esea.net/match/142005420
"""


class CrawlSpider(scrapy.Spider):
    name = 'crawl'
    allowed_domains = ['play.esea.net']
    start_urls = ['https://play.esea.net/match/12500000']

    def parse(self, response):
        print(response.text)
