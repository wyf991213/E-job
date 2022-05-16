1  # !/usr/bin/env python
2  # -*- coding: utf-8 -*-
3  # @File  : handle_excel.py
4  # @Author: 王一帆
5  # @Date  : 2022/5/7
6  # @Api  :
7  # @Contact : www.yifan_wang1999@163.com
from openpyxl import load_workbook


class HandleExcel:

    def __init__(self, file_path, sheet_name):
        self.wb = load_workbook(file_path)
        self.sh = self.wb[sheet_name]

    def __read_titles(self):
        titles = []
        for item in list(self.sh.rows)[0]:  # 遍历第1行当中每一列
            titles.append(item.value)
        return titles

    def read_all_datas(self):
        all_datas = []
        titles = self.__read_titles()
        for item in list(self.sh.rows)[1:]:  # 遍历数据行
            values = []
            for val in item:  # 获取每一行的值
                values.append(val.value)
            res = dict(zip(titles, values))  # title和每一行数据，打包成字典

            all_datas.append(res)
        return all_datas

    def close_file(self):
        self.wb.close()


if __name__ == '__main__':
    he = HandleExcel("ejob.xlsx", "ejob")
    cases = he.read_all_datas()
