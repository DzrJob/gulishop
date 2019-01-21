from django.shortcuts import render
from random import choice
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler
from gulishop.settings import YUNPIAN_KEY
from users.models import VerifyCode, UserProfile
from users.serializer import VerifyCodeSerializer, UserSerializer
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


class UserViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

    # 默认的不会给mobile存数据，也不会给密码加密 需要重写
    def create(self, request, *args, **kwargs):
        # request.data returns the parsed content of the request body. This is similar to the standard request.POST and request.FILES
        # request.query_params is a more correctly named synonym for request.GET
        # 验证
        serializer = self.get_serializer(data=request.data)
        # 是否合法
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = UserProfile()
        user.username = username
        user.mobile = username
        user.set_password(password)
        user.save()
        # 如果你需要注册后直接就是登陆状态，那么你需要把token手动生成 返回给前端进行设置
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        ret = serializer.data
        ret['name'] = user.name if user.name else user.username
        ret['token'] = token

        return Response(ret, status=status.HTTP_201_CREATED)