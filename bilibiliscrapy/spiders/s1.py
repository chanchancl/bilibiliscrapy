# -*- coding: utf-8 -*-
import scrapy
import json
import time
from bilibiliscrapy.translate import text2number
from bilibiliscrapy.items import BilibiliscrapyItem

template = 'http://bangumi.bilibili.com/web_api/season/index?page={page}&page_size=20&version=0&is_finish=0&start_year=0&quarter=0&tag_id=&index_type=1&index_sort=0' 

#scrapy shell "http://bangumi.bilibili.com/web_api/season/index?page=1&page_size=40&version=0&is_finish=0&start_year=0&quarter=0&tag_id=&index_type=1&index_sort=0"

class S1Spider(scrapy.Spider):
    name = "s1"
    allowed_domains = ["bangumi.bilibili.com/"]
    end_of_page = 160
    start_urls = [ template.format(page=x) for x in range(1, end_of_page)]

    def parse(self, response):
        data = json.loads(response.body.decode('utf-8'))
        li = data['result']['list']
        
        for anime in li:
            href = anime['url']
            title = anime['title']
            #print('title : %s' % title)
            #print('pub_time : %s' % anime.get('pub_time',0))
            pub_time = float(anime.get('pub_time',0))
            #print('url : %s' % href )
            yield scrapy.Request(href, meta={'title':title,'url':href,'pub_time':pub_time} ,callback=self.parse_item, dont_filter=True)

        '''with open('233.json','a') as f:
            json.dump(data, f, indent=4, separators=(',', ': '))'''
    
    def parse_item(self, response):
        item = BilibiliscrapyItem()
        item['url'] = response.meta['url']
        item['title'] = response.meta['title']
        item['pub_time'] = response.meta['pub_time']
        if item['pub_time'] < 0:
            item['pub_time'] = 0
        item['pub_time_text'] = time.localtime(item['pub_time'])
        # 总播放数
        item['total_play_text'] = response.xpath('//span[@class="info-count-item info-count-item-play"]/em/text()').extract()[0]
        item['total_play_number'] = text2number(item['total_play_text'])
        # 追番人数
        item['total_follow_text'] = response.xpath('//span[@class="info-count-item info-count-item-fans"]/em/text()').extract()[0]
        item['total_follow_number'] = text2number(item['total_follow_text'])
        # 弹幕总数
        item['total_danmu_text'] = response.xpath('//span[@class="info-count-item info-count-item-review"]/em/text()').extract()[0]
        item['total_danmu_number'] = text2number(item['total_danmu_text'])

        # print(item)
        yield item