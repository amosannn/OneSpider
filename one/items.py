# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class OneQuoteItem(scrapy.Item):
    # 期号
    vol = scrapy.Field()
    # 图片
    imageUrl = scrapy.Field()
    # 图片类型
    imageCategory = scrapy.Field()
    # 句子
    quote = scrapy.Field()
    # 日期
    publishedDate = scrapy.Field()
