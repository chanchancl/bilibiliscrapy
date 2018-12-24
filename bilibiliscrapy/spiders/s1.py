# -*- coding: utf-8 -*-
import scrapy
import json
import time
from bilibiliscrapy.translate import text2number
from bilibiliscrapy.items import BilibiliscrapyItem

listTemplate = 'https://bangumi.bilibili.com/media/web_api/search/result?season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&pub_date=-1&style_id=-1&order=3&st=1&sort=0&page={page}&season_type=1&pagesize=20'

seasonTemplate = 'https://bangumi.bilibili.com/jsonp/seasoninfo/{season_id}.ver?callback=seasonListCallback&jsonp=jsonp&_={time}'

#https://bangumi.bilibili.com/web_api/season/index_global?page={page}&page_size=20&version=0&is_finish=0&start_year=0&tag_id=&index_type=1&index_sort=0&quarter=0
#scrapy shell "https://bangumi.bilibili.com/web_api/season/index_global?page={page}&page_size=20&version=0&is_finish=0&start_year=0&tag_id=&index_type=1&index_sort=0&quarter=0"
#scrapy shell "http://bangumi.bilibili.com/anime/5806"
#scrapy shell "http://bangumi.bilibili.com/jsonp/seasoninfo/5806.ver"

class S1Spider(scrapy.Spider):
    name = "s1"
    allowed_domains = ["bangumi.bilibili.com"]
    end_of_page = 160
    start_urls = [ listTemplate.format(page=x) for x in range(1, end_of_page)]

    def parse(self, response):
        data = json.loads(response.body.decode('utf-8'))
        li = data['result']['data']
        
        # 遍历 list
        for anime in li:
            item = BilibiliscrapyItem()
            url = anime['link']
            title = anime['title']
            order = anime['order']
            pub_time = float(order.get('pub_real_time',0))
            item['season_id'] = anime.get('season_id', 0)
            yield scrapy.Request(url, meta={'title':title, 'item':item,'url':url,'pub_time':pub_time} ,callback=self.tmp, dont_filter=True)
    
    def tmp(self, response):
        m = response.meta
        url = response.xpath('//div[@class="info-title clearfix"]/a/@href')[0].extract()
        url = 'https:' + url
        yield scrapy.Request(url, meta={'title':m['title'],'item':m['item'],'url':m['url'],'pub_time':m['pub_time']}, callback=self.parse_item, dont_filter=True)
    
    def parse_item(self, response):
        item = response.meta['item']
        item['url'] = response.meta['url']
        item['title'] = response.meta['title']
        item['pub_time'] = response.meta['pub_time']
        if item['pub_time'] < 0:
            item['pub_time'] = 0
        t = time.localtime(item['pub_time'])
        item['pub_time_text'] = '{year}年{month}月{day}日'.format(year=t[0],month=t[1],day=t[2])
        # 总播放数
        item['total_play_text'] = response.xpath('//span[@class="media-info-count-item media-info-count-item-play"]/em/text()')[0].extract()
        # 追番人数
        item['total_follow_text'] = response.xpath('//span[@class="media-info-count-item media-info-count-item-fans"]/em/text()')[0].extract()
        # 弹幕总数
        item['total_danmaku_text'] = response.xpath('//span[@class="media-info-count-item media-info-count-item-review"]/em/text()')[0].extract()
        url = seasonTemplate.format(season_id=item['season_id'], time = int(time.time())*1000)
        yield scrapy.Request(url, meta={'item':item },callback=self.parse_item2)
    
    def parse_item2(self, response):
        item = response.meta['item']
        body = response.body.decode()
        # 有些body会以 seasonListCallback() 包裹
        if body.startswith('season'):
            body = body.split('(', 1)[1]
            body = body.rsplit(')', 1)[0]
        body = body.replace('\n','')
        result = json.loads(body)['result']

        #print('Right here')
        item['total_episodes'] = int(result['total_count'])
        item['total_play_number'] = int(result['play_count'])
        item['total_follow_number'] = int(result['favorites'])
        item['total_danmaku_number'] = int(result['danmaku_count'])
        
        item['coins'] = int(result['coins'])
        item['is_finish'] = result['is_finish']
        item['jp_title'] = result.get('jp_title','')
        item['bangumi_id'] = result.get('bangumi_id', '')

        # 计算一下平均值
        if item['total_episodes'] == 0:
            item['average_play'] = 0
            item['average_danmaku'] = 0
            item['average_coins'] = 0
            item['coinbiplay'] = 0
        else:
            item['average_play'] = round((item['total_play_number'] / item['total_episodes']), 0)
            item['average_danmaku'] = round((item['total_danmaku_number'] / item['total_episodes']), 0)
            item['average_coins'] = round((item['coins'] / item['total_episodes']), 0)
            item['coinbiplay'] = round((item['coins'] / item['total_play_number']),5)
        
        yield item