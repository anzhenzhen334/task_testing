"""
============================
Author:ann
Date:2020/3/10
Time:10:20
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
class TestTestcases(unittest.TestCase):
    excel = ReadWriteExcel(case_file,'testcases')
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

    def setUp(self):
        url = conf.get('env','base_url') + '/interfaces/'

        headers = eval(conf.get('env', 'headers'))
        headers['Authorization'] = getattr(CaseData, 'token_value')

        CaseData.interface_name = self.random_name()
        data = '{ "name": "接口#interface_name#", "tester": "ann", "project_id": #pid#, "desc": "这是一个接口描述" }'
        data = replace_data(data)
        data = eval(data)

        response = self.request.send_request(url=url, method='post', json=data,headers=headers)
        content = eval(response.content.decode('utf-8'))
        CaseData.interface_id = str(content['id'])

    @data(*cases)
    def test_testcases(self,case):
        headers = eval(conf.get('env','headers'))
        headers['Authorization'] = getattr(CaseData,'token_value')

        url = conf.get('env','base_url') + case['url']
        method = case['method']
        CaseData.testcase_name = self.random_name()
        case['data'] = replace_data(case['data'])
        data = eval(case['data'])

        expected = eval(case['expected'])
        row = case['case_id'] + 1

        response = self.request.send_request(url=url, method=method, json=data,headers=headers)
        status_code = response.status_code
        print('执行接口后状态码是：', status_code)

        res = response.json()
        print('执行接口后的响应结果是：',res)

        # content = response.content.decode('utf-8')
        if status_code == 201:
            # content = eval(content)
            # print('接口成功的接口信息为：',content)
            if case['title'] == '新增测试用例成功':
                # 如果是添加成功的接口，把用例名字取出来作为excel中第二条用例的验证（第二条用例的name用的是第一条已经添加过的那个name)
                CaseData.have_testcases_name = res['name']

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

    def random_name(self):
        name = 'ann0310'
        n = random.randint(10000, 99999)
        name += str(n)
        return name