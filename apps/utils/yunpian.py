# -*-coding:utf-8-*-
__author__ = 'Dzr'
import json
import requests


class YunPian(object):
    def __init__(self,api_key):
        self.api_key = api_key
        # 云片短信接口
        self.single_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_msg(self,mobile,code):
        data = {
            'apikey':self.api_key,
            'mobile':mobile,
            'text':'【刘渊先生】您的验证码是{code}。如非本人操作，请忽略本短信'.format(code=code)
        }
        # 根据云片规则 发送请求 得到json
        result = requests.post(url=self.single_send_url,data=data).text
        # json反序列化成字典
        result = json.loads(result)
        return result