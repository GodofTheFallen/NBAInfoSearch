import re

import scrapy


def news_text_parse(response):
    dic = {
        'id': re.findall(r"\d+", response.url)[0],
        'href': response.url,
        'title': response.css("h1.headline::text").get().replace('\n', '').replace('\r', '').replace(' ', ''),
        'time': response.css("span#pubtime_baidu::text").get(),
        'source': {
            'text': response.css("span.comeFrom a::text").get(),
            'href': response.css("span.comeFrom a::attr(href)").get()
        },
        'body': response.css("div.artical-main-content p::text").getall()
    }
    yield dic


class NewsSpider(scrapy.Spider):
    name = "news"
    page_max = 20
    
    def start_requests(self):
        url_temp = 'http://voice.hupu.com/nba/'
        
        for page in range(1, self.page_max + 1):
            yield scrapy.Request(url_temp + str(page), callback=self.parse)
    
    def parse(self, response):
        urls = response.css("div.list-hd h4 a::attr(href)").getall()
        for url in urls:
            yield scrapy.Request(url=url, callback=news_text_parse)
