# -*- coding: utf-8 -*-
import scrapy


class GameCrawlerSpider(scrapy.Spider):
    name = "game_crawler"
    allowed_domains = ["play.esea.net"]
    start_urls = (
        'https://play.esea.net/match/14113162',
    )

    def parse(self, response):
        title = response.css('.title::text').extract()
        yield {'title': title}
