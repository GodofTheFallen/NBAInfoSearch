import re
from datetime import datetime

import scrapy

from ..items import NewsPageItem


def news_text_parse(response):
    dic = {
        'id': re.findall(r"\d+", response.url)[0],
        'url': response.url,
        'title': response.css("h1.headline::text").get().replace('\n', '').replace('\r', '').replace(' ', ''),
        'time': response.css("span#pubtime_baidu::text").get(),
        'source': {
            'text': response.css("span.comeFrom a::text").get(),
            'url': response.css("span.comeFrom a::attr(href)").get()
        },
        'body': response.css("div.artical-main-content p::text").getall()
    }
    npi = NewsPageItem()
    npi['id'] = int(dic['id'])
    npi['url'] = dic['url']
    npi['title'] = dic['title']
    npi['time'] = datetime.strptime(dic['time'], ' %Y-%m-%d %H:%M:%S ')
    npi['source_name'] = dic['source']['text']
    npi['source_url'] = dic['source']['url']
    npi['body'] = dic['body']
    npi.save()
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
