# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
from pymongo import MongoClient
from datetime import datetime

class MongoPipeline(object):

    def __init__(self, items, mongo_uri):
        self.mongo_uri = mongo_uri
        self.items = items

    @classmethod
    def from_crawler(cls, crawler):
        ## pull in information from settings.py
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            items = []
        )

    def open_spider(self, spider):
        ## initializing spider
        ## opening db connection
        self.client = MongoClient(self.mongo_uri)

    def close_spider(self, spider):
        ## clean up when spider is closed
        data = self.client['scraper']
        col = data['technologies']

        new_field = col.insert_one({"offers": [], "created_at": datetime.now()})

        new_field_id = new_field.inserted_id

        for offer in self.items:
            col.update_one({"_id": new_field_id}, { "$push": { "offers": offer }})

        self.items = []
        self.client.close()

    def process_item(self, item, spider):
        ## how to handle each post
        self.items.append(dict(item))
        return item