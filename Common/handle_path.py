1  # !/usr/bin/env python
2  # -*- coding: utf-8 -*-
3  # @File  : handle_path.py
4  # @Author: 王一帆
5  # @Date  : 2022/5/7
6  # @Api  :
7  # @Contact : www.yifan_wang1999@163.com
import os

# 获取项目的路径,向上两层
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(base_dir)

# 测试用例路径
cases_dir = os.path.join(base_dir, 'TestCases')
# 测试数据路径
datas_dir = os.path.join(base_dir, 'TestDatas')
# 测试报告路径
reports_dir = os.path.join(base_dir, 'Outputs\\reports')
# 日志路径
logs_dir = os.path.join(base_dir, 'Outputs\\logs')
# 配置文件路径
conf_dir = os.path.join(base_dir, 'Conf')