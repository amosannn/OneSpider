from scrapy import Request
from scrapy.spiders import Spider

from one.items import OneQuoteItem


class OneSpider(Spider):
    name = 'one_quote'
    base_url = 'http://wufazhuce.com/one/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }

    def start_requests(self):
        for i in range(14, 19):
            url = self.base_url + str(i)
            yield Request(url, headers=self.headers)

    def parse(self, response):
        item = OneQuoteItem()
        movies = response.xpath('//div[@class="tab-content"]')
        for movie in movies:
            item['vol'] = movie.xpath(
                './/div[@class="one-imagen-footer"]/div[@class="one-titulo"]/text()').extract()[0].split('.', 1)[
                1].strip()
            item['imageUrl'] = movie.xpath(
                './/div[@class="one-imagen"]/img/@src').extract()[0].strip()
            item['imageCategory'] = movie.xpath(
                './/div[@class="one-imagen-footer"]/div[@class="one-imagen-leyenda"]/text()').extract()[0].strip()
            item['quote'] = movie.xpath(
                './/div[@class="one-cita-wrapper"]/div[@class="one-cita"]/text()').extract()[0].strip()
            item['publishedDate'] = movie.xpath(
                './/div[@class="one-cita-wrapper"]/div[@class="one-pubdate"]/p[1]/text()').extract()[0].strip() + " " + \
                                    movie.xpath(
                                        './/div[@class="one-cita-wrapper"]/div[@class="one-pubdate"]/p[2]/text()').extract()[
                                        0].strip()
            yield item

    # scrapy crawl one_quote -o one_quete.csv (export csv
    # scrapy crawl one_quote -o one_quete.json (export json
