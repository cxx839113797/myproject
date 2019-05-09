# -*- coding:utf-8 -*-
# @Time  : 2019/5/9 0:42
# @Author: xiaoxiao
# @File  : test_verifyUserAuth.py

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
from common.get_cre_id import get_cre_id
log=Logger(__name__)

@ddt
class verifyUserAuth(unittest.TestCase):
    excel = DoExcel(excel_name, "verifyUserAuth")
    s = excel.read()
    @classmethod
    def setUpClass(cls):
        log.info("准备测试")
        cls.mysql=DoMysql()
        cls.excel = DoExcel(excel_name, "verifyUserAuth")
    @data(*s)
    def test_verifyUserAuth(self,case):
        log.info("测试标题：{}".format(case.title))
        if case.data.find("$(cre_id)")>-1:
            case.data=case.data.replace("$(cre_id)",get_cre_id())
        if case.data.find("$(mobile)")>-1:
            mobile=get_mobile()
            while self.mysql.fetchOne('SELECT * FROM sms_db_53.t_mvcode_info_6 where Fmobile_no ='+mobile):
                mobile=get_mobile()
            case.data=case.data.replace("$(mobile)","#mobilephone#")
            setattr(Regulax,"mobilephone",str(mobile))
        if case.data.find("$(user_id)")>-1:
            sql="SELECT MAX(Fuid) FROM user_db.t_user_info ORDER BY Fuid DESC LIMIT 1"
            id=self.mysql.fetchOne(sql)["MAX(Fuid)"]
            id=int(id)+1
            user_id="haha"+str(id)
            case.data=case.data.replace("$(user_id)",user_id)
        if case.check_sql:
            before=self.mysql.fetchOne(case.check_sql)["MAX(Fpk_id)"]
        case.data=regulax(case.data)
        case.data=json.loads(case.data)
        case.url=config.get("pre_url","pre_url")+case.url
        log.debug("测试URL：{}".format(case.url))
        log.debug("请求参数：{}".format(case.data))
        webservice=Client(case.url,cache=None)
        try:
            try:
                if case.title == "正常发送验证码":
                    result = webservice.service.sendMCode(case.data)
                    self.excel.write(case.case_id + 1, 6, str(result))
                    sql = 'SELECT Fverify_code FROM sms_db_53.t_mvcode_info_6 WHERE Fmobile_no=' + case.data["mobile"]
                    verify_code = self.mysql.fetchOne(sql)["Fverify_code"]
                    setattr(Regulax, "verify_code", verify_code)
                elif case.title == "正常注册用户":
                    result = webservice.service.userRegister(case.data)
                    self.excel.write(case.case_id + 1, 6, str(result))
                    sql = 'SELECT Fuid FROM user_db.t_user_info WHERE Fuser_id="{0}"'.format(case.data["user_id"])
                    uid = str(self.mysql.fetchOne(sql)["Fuid"])
                    setattr(Regulax, "uid", uid)
                else:
                    result=webservice.service.verifyUserAuth(case.data)
            except WebFault as e:
                self.excel.write(case.case_id + 1, 6, str(e))
                case.expected=regulax(case.expected)
                self.assertIn(case.expected, str(e))
                self.excel.write(case.case_id + 1, 7, "Pass")
            else:
                self.assertEqual(str(result.retCode), json.loads(case.expected)["retCode"])
                self.assertEqual(str(result.retInfo), json.loads(case.expected)["retInfo"])
                if case.check_sql:
                    after = self.mysql.fetchOne(case.check_sql)["MAX(Fpk_id)"]
                    self.assertEqual(int(before)+1,int(after))
                    sql="SELECT Fcre_id FROM user_db.t_user_auth_info WHERE Fuid="+ getattr(Regulax,"uid")
                    cre_id=self.mysql.fetchOne(sql)
                    self.assertNotEqual(case.data["cre_id"],cre_id)
                if case.title=="正常认证用户":
                    cre_id=case.data["cre_id"]
                    setattr(Regulax,"cre_id",cre_id)
                self.excel.write(case.case_id + 1, 7, "Pass")
        except AssertionError as e:
            self.excel.write(case.case_id+1,7,"Fail")
            log.error("测试报错：{}".format(e))
            raise e
    @classmethod
    def tearDownClass(cls):
        log.info("测试结束")
        cls.excel.close()
        cls.mysql.close()

if __name__ == '__main__':
    unittest.main()