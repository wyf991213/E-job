import unittest
from BeautifulReport import BeautifulReport
from Common.handle_path import cases_dir, reports_dir

# 收集用例
s = unittest.TestLoader().discover(cases_dir)

# 生成报告
br = BeautifulReport(s)
br.report('E-job', '测试报告.html', reports_dir)