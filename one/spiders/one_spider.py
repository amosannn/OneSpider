# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.spiders import Spider

from one.items import OneQuoteItem
from one.items import OneArticleItem
from one.items import OneQuestionItem

import re


class QuoteSpider(Spider):
    """ 「ONE · 一个」 每日一句、每日一图爬虫

    每日一句： 爬取的内容有期号、句子、发布日期
    每日一图： 爬取的内容有图片url、图片分类

    Attributes:
        name: 爬虫名，不可重复
        base_url: 目标网址头
        url: 目标网址
        item: 映射 one.items.py
        infos: xpath提取的页面元素（未处理）
        info: 根据各个item字段提取各自元素
    """

    name = 'one_quote'
    base_url = 'http://wufazhuce.com/one/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }

    def start_requests(self):
        for i in range(14, 19):
            url = self.base_url + str(i)
            yield Request(url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        item = OneQuoteItem()
        infos = response.xpath('//div[@class="tab-content"]')
        for info in infos:
            item['vol'] = info.xpath(
                './/div[@class="one-imagen-footer"]/div[@class="one-titulo"]/text()').extract()[0].split('.', 1)[
                1].strip()
            item['imageUrl'] = info.xpath(
                './/div[@class="one-imagen"]/img/@src').extract()[0].strip()
            item['imageCategory'] = info.xpath(
                './/div[@class="one-imagen-footer"]/div[@class="one-imagen-leyenda"]/text()').extract()[0].strip()
            item['quote'] = info.xpath(
                './/div[@class="one-cita-wrapper"]/div[@class="one-cita"]/text()').extract()[0].strip()
            item['publishedDate'] = info.xpath(
                './/div[@class="one-cita-wrapper"]/div[@class="one-pubdate"]/p[1]/text()').extract()[0].strip() + " " + \
                                    info.xpath(
                                        './/div[@class="one-cita-wrapper"]/div[@class="one-pubdate"]/p[2]/text()').extract()[
                                        0].strip()
            yield item

    # scrapy crawl one_quote -o one_quete.csv (export csv
    # scrapy crawl one_quote -o one_quete.json (export json


class ArticleSpider(Spider):
    """ 「ONE · 一个」 每日一文爬虫

    每日一文： 爬取的内容有页面地址、页面id、文章标题、作者、编辑、摘要、正文
        正文使用了正则剥离外层<div>标签对
        获得的内容包含换行符(<br>)，如需去除可自行处理

    Attributes:
        name: 爬虫名，不可重复
        base_url: 目标网址头
        url: 目标网址
        item: 映射 one.items.py
        infos: xpath提取的页面元素（未处理）
        info: 根据各个item字段提取各自元素
    """

    name = 'one_article'
    base_url = 'http://wufazhuce.com/article/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }

    def start_requests(self):
        # for i in range(9, 2998):
        for i in range(33, 35):
            url = self.base_url + str(i)
            yield Request(url, headers=self.headers, callback=self.parse, meta={'url': url, 'sufNum': str(i)})

    def parse(self, response):
        item = OneArticleItem()
        infos = response.xpath('//div[@class="one-articulo"]')
        for info in infos:
            item['pageId'] = response.meta['sufNum']
            item['url'] = response.meta['url']
            item['title'] = info.xpath('.//h2[@class="articulo-titulo"]/text()').extract()[0].strip()
            item['author'] = info.xpath('.//p[@class="articulo-autor"]/text()').extract()[0].split('/', 1)[1].strip()
            item['editor'] = info.xpath('.//p[@class="articulo-editor"]/text()').extract()[0].strip()
            item['description'] = \
                info.xpath('.//div[@class="comilla-abrir"]/div[@class="comilla-cerrar"]/text()').extract()[0].strip()

            # 提取未处理文章（包含html标签）
            # 匹配html标签正则 </?\w+[^>]*>
            raw_article = info.xpath('.//div[@class="articulo-contenido"]').extract()[0]
            # 去除div标签（外壳）
            re_div = re.compile('</?div\s*[^<]*>')
            article = re_div.sub('', raw_article)
            item['article'] = article.strip()

        yield item


class QuestionSpider(Spider):
    """ 「ONE · 一个」 每日一问爬虫

    每日一问： 爬取的内容有页面地址、页面id、问题、问题简述、回答者、问答详情

    Attributes:
        name: 爬虫名，不可重复
        base_url: 目标网址头
        url: 目标网址
        item: 映射 one.items.py
        infos: xpath提取的页面元素（未处理）
        info: 根据各个item字段提取各自元素
    """

    name = 'one_question'
    base_url = 'http://wufazhuce.com/question/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }

    def start_requests(self):
        for i in range(8, 30):
            url = self.base_url + str(i)
            yield Request(url, headers=self.headers, callback=self.parse, meta={'url': url, 'pageId': str(i)})

    def parse(self, response):
        item = OneQuestionItem()
        infos = response.xpath('//div[@class="one-cuestion"]')
        for info in infos:
            item['pageId'] = response.meta['pageId']
            item['url'] = response.meta['url']
            item['question'] = info.xpath('.//h4[1]/text()').extract()[0].strip()
            item['questionContent'] = info.xpath('.//div[2]/text()').extract()[0].strip()
            item['answer'] = info.xpath('.//h4[2]/text()').extract()[0].strip()

            # 去除div标签
            raw_answer = info.xpath('.//div[4]').extract()[0]
            re_div = re.compile('</?div\s*[^<]*>')
            answer = re_div.sub('', raw_answer)
            item['answerContent'] = answer.strip()

        yield item
