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
from common.regular import regulax,Regulax
from common.get_mobile import get_mobile
import datetime
log=Logger(__name__)

@ddt
class userRegister(unittest.TestCase):
    excel = DoExcel(excel_name, "userRegister")
    s = excel.read()
    @classmethod
    def setUpClass(cls):
        log.info("准备测试")
        cls.mysql=DoMysql()
    @data(*s)
    def test_userRegister(self,case):
        log.info("测试标题：{}".format(case.title))
        if case.data.find("$(mobile)")>-1:
            mobile=get_mobile()
            while self.mysql.fetchOne('SELECT * FROM sms_db_53.t_mvcode_info_6 where Fmobile_no ='+mobile):
                mobile=get_mobile()
            case.data=case.data.replace("$(mobile)","#mobilephone#")
            setattr(Regulax,"mobilephone",str(mobile))
        if case.data.find("#user_id#")>-1:
            sql="SELECT MAX(Fuid) FROM user_db.t_user_info ORDER BY Fuid DESC LIMIT 1"
            id=self.mysql.fetchOne(sql)["MAX(Fuid)"]
            id=int(id)+1
            user_id="haha"+str(id)
            case.data=case.data.replace("#user_id#",user_id)
            setattr(Regulax,"user_id",user_id)
        if case.data.find("$(verify_code)")>-1:
            sql = "SELECT Fverify_code FROM sms_db_53.t_mvcode_info_6 WHERE Fmobile_no <>  "+ getattr(Regulax,"mobilephone")
            " AND Fexpired_time > "+str(datetime.datetime.now())
            verify_code=self.mysql.fetchOne(sql)["Fverify_code"]
            case.data=case.data.replace("$(verify_code)",verify_code)
        if case.check_sql:
            case.check_sql=regulax(case.check_sql)
            case.check_sql = eval(case.check_sql)
            before=self.mysql.fetchOne(case.check_sql["sql1"])["MAX(Fuid)"]
        case.data=regulax(case.data)
        case.data=json.loads(case.data)
        case.url=config.get("pre_url","pre_url")+case.url
        log.debug("测试URL：{}".format(case.url))
        log.debug("请求参数：{}".format(case.data))
        excel = DoExcel(excel_name, "userRegister")
        webservice = Client(case.url,cache=None)
        try:
            if case.title=="正常发送验证码":
                result=webservice.service.sendMCode(case.data)
                sql='SELECT Fverify_code FROM sms_db_53.t_mvcode_info_6 WHERE Fmobile_no='+case.data["mobile"]
                verify_code=self.mysql.fetchOne(sql)["Fverify_code"]
                setattr(Regulax,"verify_code",verify_code)
            else:
                result=webservice.service.userRegister(case.data)
            excel.write(case.case_id+1,6,str(result))
            self.assertEqual(str(result.retCode),json.loads(case.expected)["retCode"])
            self.assertEqual(str(result.retInfo), json.loads(case.expected)["retInfo"])
            if case.check_sql:
                after=self.mysql.fetchOne(case.check_sql["sql1"])["MAX(Fuid)"]
                self.assertEqual(int(before)+1,int(after))
                mobile=self.mysql.fetchOne(case.check_sql["sql2"])["Fmobile"]
                pwd=self.mysql.fetchOne(case.check_sql["sql2"])["Fpwd"]
                self.assertNotEqual(case.data["mobile"],mobile)
                self.assertNotEqual(case.data["pwd"], pwd)
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
