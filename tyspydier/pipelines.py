# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonLinesItemExporter
import datetime, json

class JsonExportPipeline(object):
    def open_spider(self, spider):
        now = datetime.datetime.now()
        file = open(now.strftime('%Y%m%d%H%M%S%f.json'), 'wb')
        self.exporter = JsonLinesItemExporter(file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.exporter.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class TyspydierPipeline(object):
    def __init__(self):
        now = datetime.datetime.now()
        self. file = open(now.strftime('%Y%m%d%H%M%S%f.json'), 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False).encode('utf8') + "\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()


