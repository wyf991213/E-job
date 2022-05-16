1  # !/usr/bin/env python
2  # -*- coding: utf-8 -*-
3  # @File  : handle_db.py
4  # @Author: 王一帆
5  # @Date  : 2022/5/7
6  # @Api  :
7  # @Contact : www.yifan_wang1999@163.com
import pymysql


class HandleDB:

    def __init__(self):
        # 连接数据库，创建游标。
        # 1、建立连接
        self.conn = pymysql.connect(
            host="139.9.71.47",
            port=3306,
            user="grand_search",
            password="Grand_search@123",
            database="center_db",
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
        # 2、创建游标
        self.cur = self.conn.cursor()

    def select_one_data(self, sql):
        self.conn.commit()
        self.cur.execute(sql)
        return self.cur.fetchone()

    def select_all_data(self, sql):
        self.conn.commit()
        self.cur.execute(sql)
        return self.cur.fetchall()

    def get_count(self, sql):
        self.conn.commit()
        return self.cur.execute(sql)

    def update(self, sql):
        """
        对数据库进行增、删、改的操作。
        :param sql:
        :return:
        """
        self.cur.execute(sql)
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()
