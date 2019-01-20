from django.shortcuts import render
from random import choice
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from gulishop.settings import YUNPIAN_KEY
from users.models import VerifyCode
from users.serializer import VerifyCodeSerializer
from utils.yunpian import YunPian


# Create your views here.


class VerifyCodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = VerifyCode.objects.all()
    serializer_class = VerifyCodeSerializer

    # 不满足我们的需求，重写create方法
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 获取注册者手机号
        mobile = serializer.validated_data['mobile']
        # 获取验证码
        code = self.get_random_code()
        # 应用云片发送验证码到注册者手机号
        yunpian = YunPian(YUNPIAN_KEY)
        res = yunpian.send_msg(mobile, code)
        # 状态码为0，成功 将注册者手机号与验证码存入表
        if res['code'] == 0:
            ver = VerifyCode()
            ver.mobile = mobile
            ver.code = code
            ver.save()
            return Response(data={'mobile': mobile, 'msg': res['msg']}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'mobile': mobile, 'msg': res['msg']}, status=status.HTTP_400_BAD_REQUEST)

    # 随机验证码方法
    def get_random_code(self):
        str = '1234567890'
        code = ''
        for i in range(6):
            code += choice(str)
        return code
