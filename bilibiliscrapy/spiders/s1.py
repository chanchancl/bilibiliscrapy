# -*- coding: utf-8 -*-
import scrapy
import json
import time
import math
import requests
import re
from scrapy.exceptions import CloseSpider
from bilibiliscrapy.items import BilibiliscrapyItem

seasonTemplate = 'https://bangumi.bilibili.com/media/web_api/search/result?season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&pub_date=-1&style_id=-1&order=3&st=1&sort=0&page={page}&season_type=1&pagesize=20'

mediaTemplate = 'https://www.bilibili.com/bangumi/media/md{media}'
infoTemplate = 'https://bangumi.bilibili.com/ext/web_api/season_count?season_id={season_id}&season_type=1&ts={time}'

class S1Spider(scrapy.Spider):
    name = "s1"
    allowed_domains = ["bilibili.com"]
    # start_urls = [
    #     seasonTemplate.format(page = 1)
    # ]

    def start_requests(self):
        tx = requests.get(seasonTemplate.format(page=1)).text
        rawJson = json.loads(tx)
        pageData = rawJson['result']['page']
        totalPage = math.ceil((pageData['total'] / pageData['size']))
        for i in range(1, totalPage + 1):
            yield scrapy.Request(seasonTemplate.format(page = i))

    def parse(self, response):
        rawJson = json.loads(response.body)
        # get all item page
        seasonList = rawJson["result"]["data"]
        
        for data in seasonList:
            item = BilibiliscrapyItem()
            item['title'] = data['title']
            item['link']   = data['link']
            item['season_id'] = data['season_id']
            item['pub_time']  = data['order'].get('pub_real_time', 0)
            item['is_finish'] = data['is_finish']
            item['score'] = float(data['order'].get('score','00')[:-1])
            media_id = data['media_id']
            
            next_url = mediaTemplate.format(media=media_id)
            yield scrapy.Request(url = next_url, callback=self.parse_textinfo, meta={'item':item})


    def parse_textinfo(self, response):
        item = response.meta['item']
        if item['pub_time'] < 0:
            item['pub_time'] = 0
        t = time.localtime(item['pub_time'])
        item['pub_time_text'] = '{year}年{month}月{day}日'.format(year=t[0],month=t[1],day=t[2])
        # 总播放数
        item['total_view_text'] = response.xpath('//span[@class="media-info-count-item media-info-count-item-play"]/em/text()')[0].extract()
        # 追番人数
        item['total_favorite_text'] = response.xpath('//span[@class="media-info-count-item media-info-count-item-fans"]/em/text()')[0].extract()
        # 弹幕总数
        item['total_danmaku_text'] = response.xpath('//span[@class="media-info-count-item media-info-count-item-review"]/em/text()')[0].extract()

        body = response.body.decode()
        j = re.search('window.__INITIAL_STATE__=(.*);\(function\(\)', body).group(1)
        
        data = json.loads(j)
        media = data['mediaInfo']

        item['cover_url'] = media['cover']
        item['jp_title'] = media['origin_name']
        item['total_episodes']  = media['season_status']

        item['total_danmaku_number'] = media['stat']['danmakus']
        item['total_favorite_number'] = media['stat']['favorites']
        item['total_view_number'] = media['stat']['views']

        print(item['season_id'])
        url = infoTemplate.format(season_id=item['season_id'], time = int(time.time()*1000))
        yield scrapy.Request(url=url, callback=self.parse_rawinfo, meta={'item':item})
        
    def parse_rawinfo(self, response):
        rawJson = json.loads(response.body)
        item = response.meta['item']
        data = rawJson['result']
        item['coins'] = data['coins']

        if item['total_episodes'] == 0:
            item['average_view'] = 0
            item['average_danmaku'] = 0
            item['average_coins'] = 0
            item['coinbiplay'] = 0
        else:
            item['average_view'] = round((item['total_view_number'] / item['total_episodes']), 0)
            item['average_danmaku'] = round((item['total_danmaku_number'] / item['total_episodes']), 0)
            item['average_coins'] = round((item['coins'] / item['total_episodes']), 0)
            item['coinbiplay'] = round((item['coins'] / item['total_view_number']),5)

        yield item
        