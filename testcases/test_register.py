"""
============================
Author:ann
Date:2020/3/9
Time:12:45
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
class TestRegister(unittest.TestCase):
    excel = ReadWriteExcel(case_file,'register')
    cases = excel.read_excel()
    request = HandlerRequests()

    @data(*cases)
    def test_register(self,case):
        """

        :param case: 入参中的case指的是把cases（读取excel的数据）拆包，得到一条一条的用例
        :param CaseData.random_username 调用随机方法，生成username，放在CaseData类中，作为类属性，在replace_data方法中实施替换
        :param data=eval(case['data'] 取到excel中case['data']的类型是字符串，字符串里面是字典，通过eval识别出字符串中的python表达式，得到字典
        :param response.status_code得到响应的状态码；response.content得到byte类型的类型（使用response.content.decode('utf-8')转换），response.text得到文本形式的内容
        :return:
        """
        url = conf.get('env','base_url') + case['url']
        method = case['method']

        CaseData.random_username = self.random_user()
        CaseData.random_email = self.random_email()
        case['data'] = replace_data(case['data'])
        data = eval(case['data'])

        expected = eval(case['expected'])
        row = case['case_id'] + 1

        response = self.request.send_request(url=url, method=method, json=data)
        status_code = response.status_code
        print('执行接口后状态码是：', status_code)

        res = response.json()
        print('接口响应结果是：',res)

        # content = response.content.decode('utf-8')
        # if status_code == 201:
        #     content = eval(content)
        #     print('注册成功的接口信息为：',content)

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

    def random_user(self):
        user_name = 'ann'
        n = random.randint(100,9999999)
        user_name += str(n)
        return user_name
    def random_email(self):
        mail_host = random.choice([126, 163, 139, 'qq'])
        n = random.randint(100,999999)
        email = str(n) + '@' + str(mail_host) + '.com'
        return email
