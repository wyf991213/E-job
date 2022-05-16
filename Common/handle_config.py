1  # !/usr/bin/env python
2  # -*- coding: utf-8 -*-
3  # @File  : handle_config.py
4  # @Author: 王一帆
5  # @Date  : 2022/5/7
6  # @Api  :
7  # @Contact : www.yifan_wang1999@163.com
import os
from configparser import ConfigParser
from Common.handle_path import conf_dir


class HandleConfig(ConfigParser):

    def __init__(self, file_path):
        super().__init__()
        self.read(file_path, encoding="utf-8")


file_path = os.path.join(conf_dir, 'ejob.ini')
conf = HandleConfig(file_path)
print(conf.get('log', 'name'))
