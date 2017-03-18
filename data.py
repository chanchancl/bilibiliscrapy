
import json
import xlwt
from collections import OrderedDict
f = open('items.json', 'r')


def getjson():
    while True:
        line  = f.readline()
        if line:
            yield json.loads(line, object_pairs_hook=OrderedDict)
        else:
            break


data = [x for x in getjson()]

# 按播放数，降序排序
b = sorted(data, key=lambda d : d['total_play_number'], reverse=True)

f = xlwt.Workbook()

sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)

for i,anime in enumerate(data):
    for j,item in enumerate(anime.values()):
        if isinstance(item, float):
            item = int(item)
        sheet1.write(i, j, str(item))

f.save('items.xls')