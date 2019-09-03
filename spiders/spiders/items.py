# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from main.models import NewsPage


class SpidersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


from scrapy_djangoitem import DjangoItem


class NewsPageItem(DjangoItem):
    django_model = NewsPage
