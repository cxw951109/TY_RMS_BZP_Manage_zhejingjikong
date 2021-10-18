from django.test import TestCase
from django.test.client import Client


class DrugTest(TestCase):
    a = Client()
    a.post('/account/login?userAccount=admin&userPassword=admin')


    def setUp(self):
        print('测试开始中。。。')

    def tearDown(self):
        print('测试结束。。。。')
