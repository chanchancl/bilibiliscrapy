# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BilibiliscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    pub_time = scrapy.Field()
    pub_time_text = scrapy.Field()
    total_play_text = scrapy.Field()
    total_play_number = scrapy.Field()
    total_follow_text = scrapy.Field()
    total_follow_number = scrapy.Field()
    total_danmu_text = scrapy.Field()
    total_danmu_number = scrapy.Field()
    pass