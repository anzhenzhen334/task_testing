"""
============================
Author:ann
Date:2020/3/9
Time:14:52
E-mail:326329411@qq.com
Mobile:15821865916
============================
"""
import unittest
import os
from common.read_write_excel import ReadWriteExcel
from common.handlerpath import DATA_DIR
from library.ddt import ddt,data
from common.handlerrequests import HandlerRequests
from common.handlerconfig import conf
from common.handlerdata import CaseData,replace_data
from common.handlerlog import log


case_file = os.path.join(DATA_DIR,'apicases.xlsx')

@ddt
class TestLogin(unittest.TestCase):
    excel = ReadWriteExcel(case_file,'login')
    cases = excel.read_excel()
    request = HandlerRequests()

    @data(*cases)
    def test_login(self,case):
        url = conf.get('env','base_url') + case['url']
        method = case['method']

        CaseData.username = conf.get('test_data','username')
        CaseData.password = conf.get('test_data','password')
        case['data'] = replace_data(case['data'])
        data = eval(case['data'])

        expected = eval(case['expected'])
        row = case['case_id'] + 1

        response = self.request.send_request(url=url, method=method, json=data)
        status_code = response.status_code
        print('执行接口后状态码是：', status_code)

        content = response.content.decode('utf-8')
        if status_code == 200:
            content = eval(content)
            print('登录成功的接口信息为：',content)

        try:
            self.assertEqual(status_code,expected['status_code'])
        except Exception as e:
            self.excel.write_excel(row=row,column=8,value='未通过')
            log.error('测试用例{}执行未通过'.format(case['title']))
            log.exception(e)
            raise e
        else:
            self.excel.write_excel(row=row, column=8, value='通过')
            log.error('测试用例{}执行通过'.format(case['title']))
