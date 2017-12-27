# -*- coding: utf-8 -*-

import copy

import pymysql
import pymysql.cursors
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi


class QuotePipeline(object):

    def __init__(self, dbpool):  # dbpool是 from_setting 下面得到的
        self.dbpool = dbpool

    @classmethod  # 类方法，无需实例化就可以调用
    def from_settings(cls, settings):  # 名称固定 会被scrapy调用 直接可用setting的值
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        return cls(dbpool)

    def process_item(self, item, spider):
        asynItem = copy.deepcopy(item)
        if(spider.name) == 'one_quote':
            query = self.dbpool.runInteraction(self._conditional_insert, asynItem)  # 调用插入的方法 Interaction(中文是交互)
            query.addErrback(self._handle_error, asynItem, spider)  # 调用异常处理方法
            return asynItem
        if(spider.name)=='one_article':
            query = self.dbpool.runInteraction(self._article_insert, asynItem)  # 调用插入的方法 Interaction(中文是交互)
            query.addErrback(self._handle_error, asynItem, spider)  # 调用异常处理方法
            return asynItem

    def _conditional_insert(self, tx, item):
        sql = "INSERT INTO `one`.`quote_image` (`id`, `vol`, `quote`, `image_url`, `image_category`, `published_date`) VALUES(null, %s,%s,%s,%s,%s)"
        params = (item["vol"], item["quote"], item["imageUrl"], item["imageCategory"], item["publishedDate"])
        tx.execute(sql, params)

    def _article_insert(self, tx, item):
        sql="INSERT INTO `one`.`one_article_test` (`id`, `page_id`, `url`, `title`, `author`, `editor`, `description`, `article`) VALUES (null, %s, %s, %s, %s, %s, %s, %s)"
        params = (item["pageId"], item["url"], item["title"], item["author"], item["editor"], item["description"], item["article"])
        tx.execute(sql, params)

    def _handle_error(self, failue, item, spider):
        print(failue)
