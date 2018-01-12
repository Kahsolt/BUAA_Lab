# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from NGproject.settings import MONGODB_COLLECTION


class MongoDBPipeline(object):

    collection_name = MONGODB_COLLECTION

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGODB_URI'),
            mongo_db=crawler.settings.get('MONGODB_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if self.db[self.collection_name].find_one({"word" : item['word']}) is None:
            newDoc = {
                "word": item['word'],
                "item": [{item['item']: item['link']}]
            }
            self.db[self.collection_name].insert(newDoc)
        else:
            self.db[self.collection_name].update_one({"word" : item['word']},
                                                     {'$push': {'item': {item['item']: item['link']}}})
        return item