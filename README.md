# Bilibili scrapy

> A tool to scrapy data from bilibili.com based on scrapy.
> 一个用来爬取B站数据的爬虫，基于scrapy.
## Overview

* 目前只能爬取所有B站仍登记的官方番剧，大概有2700+
* 可爬取的数据有 
  * 番剧名称
  * 番剧的B站页面URL
  * 上映时间
  * 总播放量
  * 追番人数
  * 弹幕总数

## Get and Run

* You should install library scrapy.
* clone or download the responsity from github.
* cd the dictory,and type ```scrapy crawl s1```
* the data will be a json file named items.json

***

* 你需要安装 ```scrapy``` 这个爬虫框架库，windows安装比较麻烦,具体google一下.
* 克隆或者下载这个库到本地.
* 切换到库的目录，运行命令 ```scrapy crawl s1```
* 最终得到的数据是名为 items.json 的json文件。
