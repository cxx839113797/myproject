# -*- coding:utf-8 -*-
# @Time  : 2019/5/9 3:52
# @Author: xiaoxiao
# @File  : get_mobile.py
import random
from common.config import config

def get_mobile():
    num_start = ['134', '135', '136', '137', '138', '139', '150', '151', '152', '158', '159', '157', '182',
                 '187', '188', '147', '130', '131', '132', '155', '156', '185', '186', '133', '153', '180', '189']
    start = random.choice(num_start)
    middle = random.randint(10000, 99999)
    end=config.get("data","mobile_last_three")
    mobile = start + str(middle)+end
    return mobile
