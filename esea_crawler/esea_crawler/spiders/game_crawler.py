# -*- coding: utf-8 -*-
import cfscrape
import scrapy
from requests import Request


class GameCrawlerSpider(scrapy.Spider):
    name = "game_crawler"
    allowed_domains = ["play.esea.net",
                       'www.google.com']
    start_urls = (
        'https://play.esea.net/match/14113162',
        # 'https://www.google.com',
    )

    def start_requests(self):
        cf_requests = []
        for url in self.start_urls:
            token, agent = cfscrape.get_tokens(
                url,
                'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0')
            cf_requests.append(Request(url=url,
                                       cookies={'__cfduid': token['__cfduid']},
                                       headers={'User-Agent': agent}))
        return cf_requests

    def parse(self, response):
        # title = response.css('.title::text').extract()
        yield {'title': response.text}
