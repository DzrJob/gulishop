# -*-coding:utf-8-*-
from rest_framework.validators import UniqueValidator

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
            if (datetime.now() - verify_code[0].add_time).seconds <= 60:
                raise serializers.ValidationError('验证码发送间隔为1分钟')
            verify_code[0].delete()
        return mobile

    class Meta:
        model = VerifyCode
        fields = ['mobile']


class UserSerializer(serializers.ModelSerializer):
    # validators验证器 集合中验证唯一
    username = serializers.CharField(required=True,max_length=30,min_length=11,
                                     validators=[UniqueValidator(queryset=UserProfile.objects.all())])
    # write_only 只允许验证，不允许序列化
    # style 避免明文密码
    password = serializers.CharField(required=True,max_length=20,min_length=6,write_only=True,style={'input_type':'password'})
    code = serializers.CharField(required=True, max_length=6, min_length=6, write_only=True)

    # code验证方法
    def validate_code(self,code):
        # 输入的用户名进来验证之前的数据存在initial_data中
        mobile = self.initial_data['username']
        verify_code = VerifyCode.objects.filter(mobile=mobile,code=code)
        if verify_code:
            if (datetime.now()-verify_code[0].add_time).seconds > 1800:
                raise serializers.ValidationError('验证码已经够过期，重新发送')
        else:
            raise serializers.ValidationError('手机或者验证码出错')

    class Meta:
        model = UserProfile
        fields = ['username','password','code']