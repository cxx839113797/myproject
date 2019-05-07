# -*- coding:utf-8 -*-
# @Time  : 2019/5/5 22:33
# @Author: xiaoxiao
# @File  : my_logger.py
import logging
from common.config import config
from common.contants import log_dir
import os
class Logger:
    def __init__(self,name):
        self.collect_level=config.get("log","collect_level")
        self.console_level = config.get("log", "console_level")
        self.file_level = config.get("log", "file_level")
        self.fmt=config.get("log","format",raw=True)
        self.fileName=os.path.join(log_dir,"case.log")

        self.log= logging.getLogger(name)
        self.log.setLevel(self.collect_level)

        format = logging.Formatter(self.fmt)
        file_handler = logging.FileHandler(self.fileName, encoding="utf-8")
        file_handler.setLevel(self.file_level)
        file_handler.setFormatter(format)
        self.log.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.collect_level)
        console_handler.setFormatter(format)
        self.log.addHandler(console_handler)
    def debug(self,msg):
         return self.log.debug(msg)
    def info(self,msg):
         return self.log.info(msg)
    def warning(self,msg):
        return self.log.warning(msg)
    def error(self,msg):
        return self.log.error(msg)
    def critical(self,msg):
        return self.log.critical(msg)


