# -*- coding:utf-8 -*-
# @Time  : 2019/5/5 19:57
# @Author: xiaoxiao
# @File  : regulax.py

import re
from common.config import config
import configparser
class Regulax:
    data=None

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
                raise e
        data = re.sub(p, params, data, count=1)
    return data

