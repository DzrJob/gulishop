from django.shortcuts import render
from random import choice
from rest_framework import mixins, viewsets, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler
from gulishop.settings import YUNPIAN_KEY
from users.models import VerifyCode, UserProfile
from users.serializers import VerifyCodeSerializer, UserSerializer, UserDetailSerializer
from utils.permissions import IsOwnerOrReadOnly
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


class UserViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = UserProfile.objects.all()
    # serializer_class = UserSerializer

    # 认证
    # 一般都不会配置全局配置，token过期或不过期,都允许查看某些资源
    # 需要局部添加认证信息
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    # 权限
    # 只允许经过身份验证的用户访问。
    # 允许访问对象级权限，只允许对象的所有者编辑它。可不写
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_object(self):
        '''
        获取某个用户的时候，无论填什么样的id，拿到的永远是当前登陆的用户
        :return:
        '''
        return self.request.user

    def get_serializer_class(self):
        '''
        动态的配置序列化，根据创建与其他操作配置，序列化UserSerializer，UserDetailSerializer
        :return:
        '''
        if self.action == 'create':
            return UserSerializer
        else:
            return UserDetailSerializer

    def get_permissions(self):
        """
        动态权限配置，根据创建与其他操作配置（创建用户时候没办法要求用户处于登录状态）
        实例化并返回此视图所需的权限列表。
        """
        if self.action == 'create':
            return []
        else:
            return [permission() for permission in self.permission_classes]

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
