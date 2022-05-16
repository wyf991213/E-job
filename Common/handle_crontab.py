1  # !/usr/bin/env python
2  # -*- coding: utf-8 -*-
3  # @File  : handle_crontab.py
4  # @Author: 王一帆
5  # @Date  : 2022/5/7
6  # @Api  :
7  # @Contact : www.yifan_wang1999@163.com
# from Common.handle_crontab import get_cron_prev
#
# a = '5 * * * *'
# b = get_cron_prev(a)
# print(b)
#
#
import sched

from croniter import croniter
from datetime import datetime, timedelta

week_day_dict = {
    1: 7,
    2: 1,
    3: 2,
    4: 3,
    5: 4,
    6: 5,
    7: 6
}


# "计算定时任务下次运行时间
# sched str: 定时任务时间表达式
# timeFormat str: 格式为"%Y-%m-%d %H:%M"
# queryTimes int: 查询下次运行次数
# "
# try:
#     now = datetime.datetime.now()
# except ValueError:
#     raise
# else:
#     # 以当前时间为基准开始计算
#     cron = croniter.croniter(sched, now)
#     return [cron.get_next(datetime.datetime).strftime(timeFormat) for i in range(queryTimes)]

class MyCroniter(croniter):
    def __init__(self, expr_format, start_time=None, ret_type=float,
                 day_or=True):
        # 秒 分 时 日 月 星期 年
        expr_format = expr_format.strip()
        expr_format = self.get_year(expr_format)
        expr_format = self.get_second(expr_format)
        expr_format = self.get_week(expr_format)
        # 如果以？结尾则设置day_or = false 不匹配星期
        if expr_format.endswith('?'):
            expr_format = expr_format.replace("?", "*")
            day_or = False
        else:
            # 如果？不在结尾则说明是日期为？
            if "?" in expr_format:
                expr_format = expr_format.replace("?", "*")

        self.next_date = None
        self.second_index = 0
        super(MyCroniter, self).__init__(" ".join(expr_format.split(" ")[1:]), datetime.now(), ret_type, day_or)

    def get_next_second(self, ret_type=None):
        # 如果秒数为*，则每次next加一秒，直到59秒调用self._get_next
        # 否则直接在秒位加上 应该的秒数
        try:
            if len(self.second) == 1 and self.second[0].isdigit():
                self.next_date = self._get_next(ret_type or self._ret_type, is_prev=False)
                self.next_date += + timedelta(seconds=int(self.second[0]))
            else:
                if not self.next_date:
                    self.next_date = self._get_next(ret_type or self._ret_type, is_prev=False)
                if "all" in self.second:
                    if self.next_date.strftime("%S") == '59':
                        self.next_date = self._get_next(ret_type or self._ret_type, is_prev=False)
                    else:
                        self.next_date = self.next_date + timedelta(seconds=1)
                else:
                    if int(self.next_date.strftime("%S")) >= int(self.second[-1]):
                        self.next_date = self._get_next(ret_type or self._ret_type, is_prev=False)
                        self.second_index = 0
                        # self.next_date = self.next_date + timedelta(seconds=int(self.second[self.second_index]))
                    # else:
                    if self.second_index == 0:
                        self.next_date = self.next_date + timedelta(seconds=int(self.second[self.second_index]))
                    else:
                        self.next_date = self.next_date - timedelta(seconds=int(self.second[self.second_index - 1]))
                        self.next_date = self.next_date + timedelta(seconds=int(self.second[self.second_index]))
                    self.second_index += 1

        except Exception as e:
            print("格式错误 : {}".format(e))

    def get_year(self, expr_format):
        if len(expr_format.split(" ")) == 6:  # 如果缺少 年  就相当于年为*
            self.year = ["all"]
        elif expr_format.endswith('*'):  # 任意年都可以
            expr_format = " ".join(expr_format.split(" ")[:-1])
            self.year = ["all"]
        else:
            self.year = expr_format.split(" ")[-1]
            expr_format = " ".join(expr_format.split(" ")[:-1])
            if "-" in self.year:
                temp_year = self.year.split("-")
                self.year = list()
                for year in range(int(temp_year[0]), int(temp_year[1]) + 1):
                    self.year.append(str(year))
            elif "," in self.year:
                self.year = self.year.split(",")
            elif "/" in self.year:
                temp_year = self.year.split("/")
                self.year = list()
                for year in range(int(temp_year[0]), 2100, int(temp_year[1])):
                    self.year.append(str(year))
            else:
                self.year = [self.year]

        return expr_format

    def get_second(self, expr_format):
        if expr_format.startswith('*'):
            self.second = ["all"]
        else:
            self.second = expr_format.split(" ")[0]
            if "-" in self.second:
                temp_second = self.second.split("-")
                self.second = list()
                for second in range(int(temp_second[0]), int(temp_second[1]) + 1):
                    self.second.append(str(second))
            elif "," in self.second:
                self.second = self.second.split(",")
            elif "/" in self.second:
                temp_second = self.second.split("/")
                self.second = list()
                for second in range(int(temp_second[0]), 59, int(temp_second[1])):
                    self.second.append(str(second))
            else:
                self.second = [self.second]

        return expr_format

    def get_week(self, expr_format):
        global week_day_dict
        week = expr_format.split(" ")[-1]
        result = ""
        for item in week:
            if item.isdigit():
                result += str(week_day_dict[int(item)])
            else:
                result += item
        temp_list = expr_format.split(" ")
        temp_list[-1] = result
        return " ".join(temp_list)

    def get_next(self, ret_type=None):
        self.get_next_second(ret_type)
        if "all" in self.year:
            return self.next_date
        else:
            while True:
                if self.next_date.strftime("%Y") in self.year:
                    return self.next_date
                else:
                    if self.next_date.strftime("%Y") > self.year[-1]:
                        return None
                    else:
                        self.get_next_second(ret_type)


iter = None
CRON = ""


def cron_to_date(cron):
    # 0 0 12 ? * 3 : 秒 分 时 日 月 星期
    # tmp = cron.replace('?', '*')

    global iter
    global CRON
    if not iter or CRON != cron:
        iter = MyCroniter(cron)
        CRON = cron
    next_time = iter.get_prev(datetime)
    if next_time:
        return next_time
    else:
        return ''


if __name__ == '__main__':

    print(cron_to_date("0 5 * * * ?"))

