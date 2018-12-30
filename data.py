
import time
import json
import xlwt
from collections import OrderedDict


# 一个生成器，用于获得json中的所有记录
def getjson():
    with open('items.json', 'r') as f:
        while True:
            line  = f.readline()
            if line:
                yield json.loads(line, object_pairs_hook=OrderedDict)
            else:
                break

# 按照下面的顺序(列) 生成表格
Order = OrderedDict()
#  key  ,  header
#  Item的Filed Name, 在 Header显示的名字
Order['title'] = '番剧名称'
Order['total_view_number'] = '总播放量'
Order['total_favorite_number'] = '追番人数'
Order['total_danmaku_number'] = '弹幕总数'
Order['pub_time_text'] = '放送时间'
Order['coins'] = '硬币数'
Order['total_episodes'] = '总集数'
Order['average_view'] = '平均播放量'
Order['average_danmaku'] = '平均弹幕量'
Order['average_coins'] = '平均硬币数'
Order['coinbiplay'] = '币播比' 
Order['total_view_text'] = '总播放量'
Order['total_favorite_text'] = '追番人数'
Order['total_danmaku_text'] = '弹幕总数'
Order['season_id'] = 'Season ID'
Order['jp_title'] = '日文名称'
Order['pub_time'] = '放送时间(Epoch)'
Order['cover_url'] = '封面地址'

# 按播放数，降序排序
# b = sorted(data, key=lambda d : d['total_play_number'], reverse=True)

data = [x for x in getjson()]

f = xlwt.Workbook()
sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)

# 写入第一行
for x, key in enumerate(Order.keys()):
    sheet1.write(0, x, Order[key])

# 遍历所有每条数据
for i,anime in enumerate(data):
    # 按Order的顺序遍历数据中的每个字段
    for j,itemkey in enumerate(Order.keys()):
        # 获得实际值
        item = anime[itemkey]
        # 在单元格 i+1列，j行 写入数据  (空过首行)
        if itemkey.startswith('average'):
            item = round(item, 0)
        sheet1.write(i+1, j, str(item))

filename = time.strftime("Items %Y-%m-%d(%H-%M-%S).xls")
f.save(filename)
