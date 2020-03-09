"""
============================
Author:ann
Date:2020/3/9
Time:10:52
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
class TestUser(unittest.TestCase):
    excel = ReadWriteExcel(case_file,'user')
    cases = excel.read_excel()
    request = HandlerRequests()

    @data(*cases)
    def test_user(self,case):
        CaseData.random_username = self.random_user()
        case['url'] = replace_data(case['url'])
        url = conf.get('env','base_url') + case['url']
        print('检验用户名是否注册接口的url地址是：', url)
        method = case['method']
        data = eval(case['data'])
        expected = eval(case['expected'])
        row = case['case_id'] + 1

        response = self.request.send_request(url=url, method=method, params=data)
        # res = response.json()
        status_code = response.status_code
        print('执行接口后状态码是：', status_code)

        content = response.content
        # 上面得到一个byte类型的数据b'{"email":"370747@139.com","count":0}'
        content = content.decode('utf-8')
        # 经过decode得到一个str类型的数据'{"email":"370747@139.com","count":0}'
        if status_code == 200:
            content = eval(content)

        try:
            self.assertEqual(status_code,expected['status_code'])
            if status_code == 200:
                self.assertEqual(content['count'],expected['count'])
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
        n = random.randint(100,999999999)
        user_name += str(n)
        return user_name
