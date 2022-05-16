1  # !/usr/bin/env python
2  # -*- coding: utf-8 -*-
3  # @File  : handle_judge.py
4  # @Author: 王一帆
5  # @Date  : 2022/5/7
6  # @Api  :
7  # @Contact : www.yifan_wang1999@163.com
from Common.handle_logger import logger


# 判断api pm25 pm10
def airborne(self):
    list_true = {}

    # 判断aqi
    if self['aqi'] == None:
        logger.info('aqi为空值')
    else:
        list_true['aqi'] = 0 < int(self['aqi']) < 499

    # 判断pm25
    if self['pm25'] == None:
        logger.info('pm25为空值')
    else:
        list_true['pm25'] = 0 < int(self['pm25']) < 499

    # 判断pm10
    if self['pm10'] == None:
        logger.info('pm10为空值')
    else:
        list_true['pm10'] = 0 < int(self['pm10']) < 499

    # 判断pm10和pm25的大小
    if self['pm10'] == None or self['pm10'] == None:
        logger.info('pm10或pm25为空值')
    else:
        list_true['pm10 to pm25'] = 0 < int(self['pm25']) < int(self['pm10']) < 499

    # 判断pm10的最大值
    if self['pm10_max'] == None:
        logger.info('pm10_max为空')
    else:
        list_true['pm10_max'] = 0 < int(self['pm10']) <= int(self['pm10_max']) < 500

    if self['pm25_max'] == None:
        logger.info('pm25_max为空')
    else:
        list_true['pm25_max'] = 0 < int(self['pm25']) <= int(self['pm25_max']) < 500

    return list_true


# 判断湿度 气压 温度 紫外线 能见度
def weather(self):
    list_true = {}
    # 判断湿度
    if self['humidity'] == None:
        logger.info('湿度为空值')
    else:
        list_true['humidity'] = 0 <= int(self['humidity']) <= 100

    # 判断气压
    if self['pressure'] == None:
        logger.info('气压为空值')
    else:
        list_true['pressure'] = 500 <= int(self['pressure']) <= 1500

    # 判断体感温度
    if self['real_feel'] == None:
        logger.info('体感温度为空值')
    else:
        list_true['real_feel'] = -30 <= int(self['real_feel']) <= 50

    # 判断温度
    if self['temp'] == None:
        logger.info('温度为空值')
    else:
        list_true['temp'] = -30 <= int(self['temp']) <= 50

    # 判断紫外线强度
    if self['uvi'] == None:
        logger.info('紫外线强度为空值')
    else:
        list_true['uvi'] = 0 <= int(self['uvi']) <= 15

    # 判断能见度
    if self['vis'] == None:
        logger.info('能见度为空值')
    else:
        list_true['vis'] = 0 <= int(self['vis']) <= 30000

    return list_true
