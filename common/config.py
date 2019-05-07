# -*- coding:utf-8 -*-
# @Time  : 2019/5/5 18:34
# @Author: xiaoxiao
# @File  : config.py

from configparser import ConfigParser
from common.contants import global_dir,online_dir,test_dir

class Config:
    def __init__(self):
        self.config=ConfigParser()
        self.config.read(global_dir)
        if self.config.getboolean("switch","on"):
            self.config.read(online_dir,encoding="utf-8")
        else:
            self.config.read(test_dir,encoding="utf-8")
    def get(self,section,option,raw=False):
        return self.config.get(section,option,raw=raw)

config=Config()