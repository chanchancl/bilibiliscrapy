
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
        curnumber,length = getnumber(str[length:])
        if length != len(str):
            base = str[length]
            curnumber *= Base[base]
            length += 1 # Base 已处理
        result += curnumber
    
    return int(result)

test = [
    '8487',
    '0.999万',
    '1.1万',
    '5656.1万',
    '1.5315亿',
]

result = [
     8487,
     9990,
     11000,
     56561000,
     153150000,
]

Base = {
    '':1,
    '万':10000,
    '亿':100000000,
}


if __name__ == '__main__':
    for i in range(len(test)-1):
        number = text2number(test[i])
        if number == result[i]:
            print('Success translate %s to %s' % (test[i], number))
        else:
            print('Error! translate[%s] get %d ,but %s expected!' % (test[i],number, result[i]) )
        