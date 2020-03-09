"""
============================
Author:ann
Date:2020/3/9
Time:15:38
E-mail:326329411@qq.com
Mobile:15821865916
============================
"""
import unittest
import os
import random
from common.read_write_excel import ReadWriteExcel
from common.handlerpath import DATA_DIR
from library.ddt import ddt,data
from common.handlerrequests import HandlerRequests
from common.handlerconfig import conf
from common.handlerdata import CaseData,replace_data
from common.handlerlog import log


case_file = os.path.join(DATA_DIR,'apicases.xlsx')

@ddt
class TestProject(unittest.TestCase):
    excel = ReadWriteExcel(case_file,'projects')
    cases = excel.read_excel()
    request = HandlerRequests()

    @classmethod
    def setUpClass(cls):
        url = conf.get('env','base_url') + '/user/login/'
        data = {
            "username":conf.get('test_data','username'),
            "password":conf.get('test_data','password')
        }
        response = cls.request.send_request(url=url,method='post',json=data)
        content = eval(response.content.decode('utf-8'))
        token = content['token']
        CaseData.token_value = 'JWT' + ' ' + token

    @data(*cases)
    def test_project(self,case):
        headers = eval(conf.get('env','headers'))
        headers['Authorization'] = getattr(CaseData,'token_value')

        url = conf.get('env','base_url') + case['url']
        method = case['method']
        CaseData.project_name = self.random_project()
        case['data'] = replace_data(case['data'])
        data = eval(case['data'])

        expected = eval(case['expected'])
        row = case['case_id'] + 1

        response = self.request.send_request(url=url, method=method, json=data,headers=headers)
        status_code = response.status_code
        print('执行接口后状态码是：', status_code)

        content = response.content.decode('utf-8')
        if status_code == 201:
            content = eval(content)
            print('项目成功的接口信息为：',content)

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

    def random_project(self):
        project_name = 'ann'
        n = random.randint(10000, 99999)
        project_name += str(n)
        return project_name