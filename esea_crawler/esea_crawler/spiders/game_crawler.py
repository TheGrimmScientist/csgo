# -*- coding: utf-8 -*-
import scrapy


class GameCrawlerSpider(scrapy.Spider):
    name = "game_crawler"
    allowed_domains = ["play.esea.net"]
    start_urls = (
        'http://www.play.esea.net/',
    )

    def parse(self, response):
        pass
