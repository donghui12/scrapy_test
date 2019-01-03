# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class BoleSpliderPipeline(object):
    def __init__(self,databaseIp='localhost',databasePort=27017,user="JDH",password="123456",
                 mongodbName="local"):
        client = MongoClient(databaseIp,databasePort)
        self.db=client[mongodbName]

    def process_item(self, item, spider):
        print("这是",item)
        postItem=dict(item)
        self.db['bole'].insert_one(postItem)
        return item
