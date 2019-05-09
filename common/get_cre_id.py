# -*- coding:utf-8 -*-
# @Time  : 2019/5/9 1:32
# @Author: xiaoxiao
# @File  : last_cre_number.py

from common.config import config
import time
import random


def get_cre_id():
    start=config.get("data","cre_address_code")
    now = int(time.time())
    timeStruct = time.localtime(now)
    strTime = time.strftime("%Y%m%d", timeStruct)
    strTime=int(strTime)-200000
    middle=str(strTime)
    number=start+middle+str(random.randint(100,999))
    num = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    dict = {0: "1", 1: "0", 2: "X", 3: "9", 4: "8", 5: "7", 6: "6", 7: "5", 8: "4", 9: "3", 10: "2"}
    sum = 0
    for i in range(17):
        s = int(number[i]) * num[i]
        sum += s
    code = dict[sum % 11]
    cre_id=number+code
    return cre_id
if __name__ == '__main__':
    print(get_cre_id())
