在 Python3 中，bytes 和 str 的互相转换方式是
str.encode('utf-8')
bytes.decode('utf-8')

test_register_01: 正常注册
pt2_1: casedata的值是： {"username":"ann9186563","email":"134314@126.com","password":"an123456","password_confirm":"an123456"} <class 'str'>
data的值是： {'username': 'ann9186563', 'email': '134314@126.com', 'password': 'an123456', 'password_confirm': 'an123456'} <class 'dict'>
执行接口后状态码是： 201
注册成功的接口信息为： {'id': 595, 'username': 'ann9186563', 'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1OTUsInVzZXJuYW1lIjoiYW5uOTE4NjU2MyIsImV4cCI6MTU4MzgxNjU2NiwiZW1haWwiOiIxMzQzMTRAMTI2LmNvbSJ9.DXaDNEoLHORwP1S2PM5FHXRBvw-RO-XcblZTVLcUxig'}
