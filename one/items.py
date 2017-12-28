# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderItem(scrapy.Item):
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


class OneArticleItem(scrapy.Item):
    # 网址后缀
    pageId = scrapy.Field()
    # 来源url
    url = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 编辑
    editor = scrapy.Field()
    # 摘要
    description = scrapy.Field()
    # 正文
    article = scrapy.Field()


class OneQuestionItem(scrapy.Item):
    #网址后缀
    pageId= scrapy.Field()
    #url
    url=scrapy.Field()
    #问题
    question=scrapy.Field()
    #问题内容
    questionContent=scrapy.Field()
    #回答
    answer=scrapy.Field()
    #回答内容
    answerContent=scrapy.Field()
