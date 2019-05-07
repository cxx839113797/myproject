# -*- coding:utf-8 -*-
# @Time  : 2019/5/5 18:54
# @Author: xiaoxiao
# @File  : mysql.py

import pymysql
from common.config import config

class DoMysql:
    def __init__(self):
        host=config.get("mysql","host")
        user=config.get("mysql","user")
        pwd=config.get("mysql","pwd")
        self.mysql=pymysql.connect(host=host,user=user,password=pwd,port=3306)
        self.cursor=self.mysql.cursor(cursor=pymysql.cursors.DictCursor)
    def fetchOne(self,sql):
        self.cursor.execute(sql)
        self.mysql.commit()
        return self.cursor.fetchone()
    def fetchAll(self,sql):
        self.cursor.execute(sql)
        self.mysql.commit()
        return self.cursor.fetchall()
    def close(self):
        self.cursor.close()
        self.mysql.close()
if __name__ == '__main__':
    import datetime
    mysql=DoMysql()
    sql="SELECT * FROM sms_db_53.t_mvcode_info_6 WHERE Fmobile_no='13214164653'"
    result=mysql.fetchOne(sql)
    print(result)
    if result['Fsend_time']<result['Fexpired_time']:
        print("ok")
    if result['Fsend_time']<datetime.datetime.now():
        print(datetime.datetime.now())
    print(str(result['Fexpired_time']-result['Fsend_time'])=="0:06:00")
    mysql.close()
