"""
============================
Author:ann
Date:2020/3/9
Time:16:23
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
class TestInterface(unittest.TestCase):
    excel = ReadWriteExcel(case_file,'interfaces')
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
        url = conf.get('env','base_url') + '/projects/'

        headers = eval(conf.get('env', 'headers'))
        headers['Authorization'] = getattr(CaseData, 'token_value')

        CaseData.project_name = self.random_name()
        data = '{"name": "这是一个测试的项目编号#project_name#","leader": "ann","tester": "ann9186563","programmer": "小雅","publish_app": "自动化作业-应用","desc":"ann创建项目的描述"}'
        data = replace_data(data)
        data = eval(data)

        response = self.request.send_request(url=url, method='post', json=data,headers=headers)
        content = eval(response.content.decode('utf-8'))
        CaseData.project_id = str(content['id'])

    @data(*cases)
    def test_interface(self,case):
        headers = eval(conf.get('env','headers'))
        headers['Authorization'] = getattr(CaseData,'token_value')

        url = conf.get('env','base_url') + case['url']
        method = case['method']
        CaseData.interface_name = self.random_name()
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
            print('接口成功的接口信息为：',content)
            if case['title'] == '成功创建接口':
                # 如果是添加成功的接口，把接口名字取出来作为excel中第二条用例的验证（第二条用例的name用的是第一条已经添加过的那个name)
                CaseData.have_interface_name = content['name']

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
        name = 'ann0309'
        n = random.randint(10000, 99999)
        name += str(n)
        return name