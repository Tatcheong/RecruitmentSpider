import csv
import json
from telnetlib import Telnet

import paramiko
import pymongo
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter, JsonLinesItemExporter, JsonItemExporter


class RemoteJsonPipeline:

    def __init__(self, host, port, user, password, file_path):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.file_path = file_path
        self.client = paramiko.SSHClient()
        self.sftp = None
        self.file = None
        self.exporter = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('SSH_HOST'),
            port=crawler.settings.get('SSH_PORT'),
            user=crawler.settings.get('SSH_USER'),
            password=crawler.settings.get('SSH_PASSWORD'),
            file_path=crawler.settings.get('FILE_PATH')
        )

    def open_spider(self, spider):
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.host, self.port, self.user, self.password)
        self.sftp = self.client.open_sftp()
        self.file = self.sftp.open(self.file_path + '51job1-11.json', 'wb')
        self.exporter = JsonLinesItemExporter(self.file, encoding='utf-8')

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.file.close()
        self.client.close()


class RemoteFlumePipeline:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.tn = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('FLUME_HOST'),
            port=crawler.settings.get('FLUME_PORT')
        )

    def open_spider(self, spider):
        self.tn = Telnet(self.host, self.port)

    def process_item(self, item, spider):
        text = str(item).replace('\n', '').encode('utf-8') + b'\n'
        self.tn.write(text)
        return item

    def close_spider(self, spider):
        self.tn.close()


class MongoPipeline:

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        self.db[item.collection].insert_one(ItemAdapter(item).asdict())
        return item

    def close_spider(self, spider):
        self.client.close()
