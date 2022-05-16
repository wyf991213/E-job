1  # !/usr/bin/env python
2  # -*- coding: utf-8 -*-
3  # @File  : test_ejob.py
4  # @Author: 王一帆
5  # @Date  : 2022/5/7
6  # @Api  :
7  # @Contact : www.yifan_wang1999@163.com
import unittest
import time
import datetime

from Common.handle_excel import HandleExcel
from Common.handle_ddt import ddt, data
from Common.handle_path import datas_dir
from Common.handle_logger import logger
from Common.handle_db import HandleDB
from Common.handle_config import conf
from Common.handle_crontab import cron_to_date

he = HandleExcel(datas_dir + "\\ejob.xlsx", "ejob")
cases = he.read_all_datas()
he.close_file()
db = HandleDB()


@ddt
class TestRegister(unittest.TestCase):

    @classmethod
    def tearDownClass(cls) -> None:
        logger.info("========  执行结束  ========")
        db.close()

    @data(*cases)
    def test_register_ok(self, case):
        logger.info("*********   执行用例{}：{}   *********".format(case["id"], case["title"]))
        logger.info('此任务的执行时间为{}'.format(case['detail']))
        # 获取上一次执行时间
        prev_time = cron_to_date(case['cron'])

        # 获取配置文件中可以接受的延迟
        delay = conf.get("time", case['time'])
        dif_time = datetime.datetime.strptime(delay, '%H:%M:%S')

        # 获取全部数据
        all_data = db.select_all_data(case['sql'])
        logger.info(all_data)

        # 循环获取执行时间
        list_01 = []
        for item in range(len(all_data)):
            val = all_data[item]
            data_01 = val[case['judge']]
            str_01 = str(data_01)
            list_01.append(str_01)

        # 判断时间是否超过预期延迟
        for item, value in enumerate(list_01):
            i = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            time_difference = str(i - prev_time)
            time_diff = datetime.datetime.strptime(time_difference, '%H:%M:%S')

            # 日志输出信息
            logger.info('数据:{}为{}'.format(item + 1, all_data[item]))
            logger.info('执行时间应为：{}'.format(prev_time))
            logger.info('执行时间实际为：{}'.format(i))
            logger.info('执行时间相差：{}'.format(time_difference))
            try:
                self.assertTrue(time_diff <= dif_time)
                logger.info('断言成功')
                logger.info(' ')
            except AssertionError:
                logger.exception("断言失败！")
                logger.info(' ')
                raise
