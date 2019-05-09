# -*- coding:utf-8 -*-
# @Time  : 2019/5/9 21:46
# @Author: xiaoxiao
# @File  : run.py

import unittest
from common.contants import report_dir
import HTMLTestRunnerNew
from common.contants import case_dir

case=unittest.defaultTestLoader.discover(case_dir,"test_*.py")


with open(report_dir+"\WebService.html","wb") as f:
    runner=HTMLTestRunnerNew.HTMLTestRunner\
        ( stream=f, verbosity=2,title="这是WebService的测试报告",description="测试WebService接口",tester="xiaoxiao")
    runner.run(case)
