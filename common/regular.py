# -*- coding:utf-8 -*-
# @Time  : 2019/5/5 19:57
# @Author: xiaoxiao
# @File  : regulax.py

import re
from common.config import config
import configparser
from common.my_logger import Logger
log=Logger(__name__)
class Regulax:
    mobilephone=None

def regulax(data,p="#(.*?)#"):
    while re.search(p,data):
        result=re.search(p,data).group(1)#获取匹配到的组
        try:
            params=config.get("data",result)
        except configparser.NoOptionError as e:
            if hasattr(Regulax,result):
                params=getattr(Regulax,result)
            else:
                print("找不到参数",result)
                log.error("报错：{0},找不到参数{1}".format(e,result))
                raise e
        data = re.sub(p, params, data, count=1)
    return data

