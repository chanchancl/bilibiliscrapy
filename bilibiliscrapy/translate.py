
'''
    translate.py
    用于将含有中文记法的数字转换为阿拉伯数字

    0.1:
        目前仅支持一些非常简单的转换
        转换的例子在 test -> result 中
'''

__all__ = [
    'text2number'
]

from collections import OrderedDict

# 从str中读取一个数字（浮点数或整数）
def getnumber(str):
    length = 0
    while length < len(str):
        if str[length].isdigit() or str[length] == '.' :
            length += 1
            continue
        else:
            break

    result = float(str[:length])
    return result,length

def text2number(str):
    result = 0
    curnumber = 0
    base = ''
    length = 0
    while length < len(str):
        curnumber,tmp = getnumber(str[length:])
        length += tmp
        if length != len(str):
            base = str[length]
            curnumber *= Base[base]
            length += 1 # Base 已处理
        result += curnumber
    
    return int(result)

_UnitTest = OrderedDict({
    '8487'      : 8487,
    '0.999万'   : 9990,
    '1.1万'     : 11000,
    '5656.1万'  : 56561000,
    '1亿5000万' : 150000000,
    '1.5315亿'  : 153150000,
})

Base = {
    '':1,
    '万':10000,
    '亿':100000000,
}


if __name__ == '__main__':
    for (raw, result) in _UnitTest.items():
        number = text2number(raw)
        if number == result:
            print('Success translate %10s to %s' % (raw, number))
        else:
            print('Error! translate[%s] get %d ,but %s expected!' % (raw, number, result))
        