# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

class BilibiliscrapyPipeline(object):

    def __init__(self):
        print('open file')
        self.file = open('items.json', 'wb')
    
    def __del__(self):
        print('close file')
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line.encode())
        return item
