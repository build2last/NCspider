#-*- coding: utf-8 -*-
import re
def filter_emoji(desstr,restr=''):
    '''
    过滤表情
    '''
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)


def html_decode(tHTML):
    """
    HTML解码
    :param: url
    :return: decoded html
    """
    data = tHTML
    if data:
        charset=re.findall('encoding.*?"(\w+)"',data)
        if len(charset)>0:
            data=data.decode(charset[0])
        if "gbk" in data:
            data=data.decode("gbk")
    return data