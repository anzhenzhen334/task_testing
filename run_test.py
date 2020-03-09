"""
============================
Author:ann
Date:2020/3/9
Time:10:57
E-mail:326329411@qq.com
Mobile:15821865916
============================
"""
import unittest
import os
from common.handlerpath import CASE_DIR,REPORT_DIR
from HTMLTestRunnerNew import HTMLTestRunner

suite = unittest.TestSuite()
loader = unittest.TestLoader()
suite.addTest(loader.discover(CASE_DIR))

report_file = os.path.join(REPORT_DIR,'task_report.html')
runner = HTMLTestRunner(stream=open(report_file,'wb'),
                        description='作业接口执行结果',
                        title='接口测试报告-ann',
                        tester='ann')
runner.run(suite)