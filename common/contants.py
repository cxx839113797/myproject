# -*- coding:utf-8 -*-
# @Time  : 2019/5/5 3:27
# @Author: xiaoxiao
# @File  : contants.py

import os

base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
excel_name=os.path.join(base_dir,"data","python.xlsx")
global_dir=os.path.join(base_dir,"config","global.conf")
online_dir=os.path.join(base_dir,"config","online.conf")
test_dir=os.path.join(base_dir,"config","test.conf")
log_dir=os.path.join(base_dir,"log")

