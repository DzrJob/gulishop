# -*-coding:utf-8-*-
__author__ = 'Dzr'
import re
from datetime import datetime
from rest_framework import serializers
from gulishop.settings import MOBILE_RE
from users.models import UserProfile, VerifyCode


class VerifyCodeSerializer(serializers.ModelSerializer):

    def validate_mobile(self, mobile):
        # 第一步：判断手机是不是合法
        com = re.compile(MOBILE_RE)
        if not com.match(mobile):
            raise serializers.ValidationError('手机号不合法')
        # 第二步：判断手机是不是注册过
        if UserProfile.objects.filter(mobile=mobile):
            raise serializers.ValidationError('该手机号已被注册')
        # 第三步：判断手机是不是已经在规定时间内发送过短信
        verify_code = VerifyCode.objects.filter(mobile=mobile)
        if verify_code:
            if (datetime.now() - verify_code[0].add_time).second <= 60:
                raise serializers.ValidationError('验证码发送间隔为1分钟')
            verify_code[0].delete()
        return mobile

    class Meta:
        model = VerifyCode
        fields = ['mobile']
