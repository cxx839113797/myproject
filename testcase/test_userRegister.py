# -*- coding:utf-8 -*-
# @Time  : 2019/5/6 3:08
# @Author: xiaoxiao
# @File  : test_userRegister.py

import json
import unittest
from common.contants import excel_name
from suds import WebFault
from ddt import data, ddt
from suds.client import Client
from common.my_logger import Logger
from common.do_excel import DoExcel
from common.do_mysql import DoMysql
from common.config import config
from common.regular import regulax
import datetime
log=Logger(__name__)

@ddt
class SendMCode(unittest.TestCase):
    excel = DoExcel(excel_name, "sendMCode")
    s = excel.read()
    @classmethod
    def setUpClass(cls):
        log.info("准备测试")
        cls.mysql=DoMysql()
    @data(*s)
    def test_SendMCode(self,case):
        log.info("测试标题：{}".format(case.title))
        case.data=regulax(case.data)
        case.data=json.loads(case.data)
        case.url=config.get("pre_url","pre_url")+case.url
        log.debug("测试URL：{}".format(case.url))
        log.debug("请求参数：{}".format(case.data))
        webservice=Client(case.url)
        excel = DoExcel(excel_name, "sendMCode")
        try:
            try:
                result=webservice.service.sendMCode(case.data)
                excel.write(case.case_id+1,6,str(result))
                self.assertEqual(str(result.retCode),json.loads(case.expected)["retCode"])
                self.assertEqual(str(result.retInfo), json.loads(case.expected)["retInfo"])
                excel.write(case.case_id + 1, 7, "Pass")
                if case.check_sql:
                    case.check_sql=regulax(case.check_sql)
                    dict=self.mysql.fetchOne(case.check_sql)
                    self.assertTrue(str(dict['Fexpired_time']-dict['Fsend_time'])=="0:06:00")
                    self.assertTrue(dict['Fsend_time'] <datetime.datetime.now())
                    self.assertTrue(dict['Fexpired_time']>datetime.datetime.now())
            except WebFault as e:
                excel.write(case.case_id+1,6,str(e))
                self.assertIn(case.expected,str(e))
                excel.write(case.case_id + 1, 7, "Pass")
        except AssertionError as e:
            excel.write(case.case_id+1,7,"Fail")
            log.error("测试报错：{}".format(e))
            raise e
        finally:
            excel.close()
    @classmethod
    def tearDownClass(cls):
        log.info("测试结束")
        cls.mysql.close()

if __name__ == '__main__':
    unittest.main()
