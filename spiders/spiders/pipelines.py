# -*- coding: utf-8 -*-

import json
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

from django.db import transaction

from .items import NewsPageItem


class SpidersPipeline(object):
    def __init__(self, *args, **kwargs):
        if 'page_max' in kwargs:
            self.page_max = kwargs['page_max']
        else:
            self.page_max = 20
        self.items = []

    @transaction.atomic
    def close_spider(self, spider):
        # And here we are saving our crawled data with django models.
        for item in self.items:
            item.save()
    
    def process_item(self, item, spider):
        npi = NewsPageItem()
        npi['id'] = int(item['id'])
        npi['url'] = item['url']
        npi['title'] = item['title']
        npi['time'] = datetime.strptime(item['time'], ' %Y-%m-%d %H:%M:%S ')
        npi['source_name'] = item['source']['text']
        npi['source_url'] = item['source']['url']
        npi['body'] = json.dumps(item['body'])
        self.items.append(npi)
        return item
