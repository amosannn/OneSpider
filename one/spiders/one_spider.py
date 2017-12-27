from scrapy import Request
from scrapy.spiders import Spider

from one.items import OneQuoteItem
from one.items import OneArticleItem


class QuoteSpider(Spider):
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
    name = 'one_article'
    base_url = 'http://wufazhuce.com/article/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }

    def start_requests(self):
        # for i in range(9, 2998):
        for i in range(23, 25):
            url = self.base_url + str(i)
            yield Request(url, headers=self.headers, callback=self.parse, meta={'url':url, 'sufNum':str(i)})

    def parse(self, response):
        item = OneArticleItem()
        infos=response.xpath('//div[@class="one-articulo"]')
        for info in infos:
            item['pageId']=response.meta['sufNum']
            item['url']=response.meta['url']
            item['title']=info.xpath('.//h2[@class="articulo-titulo"]/text()').extract()[0].strip()
            item['author']=info.xpath('.//p[@class="articulo-autor"]/text()').extract()[0].strip()
            item['editor']=info.xpath('.//p[@class="articulo-editor"]/text()').extract()[0].strip()
            item['description']=info.xpath('.//div[@class="comilla-abrir"]/div[@class="comilla-cerrar"]/text()').extract()[0].strip()

            # article = info.xpath('.//div[@class="articulo-contenido"]/descendant::text()').extract()[0].strip()
            # lst = info.xpath('.//div[@class="articulo-contenido"]/br')
            # for ll in lst:
            #     article += ll.tail
            # item['article']=article
            item['article'] = info.xpath('.//div[@class="articulo-contenido"]/following::text()').extract()[0].strip()

        yield item
