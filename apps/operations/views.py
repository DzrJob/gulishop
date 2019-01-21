from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from operations.models import UserFav, UserLeavingMessage, UserAddress
from operations.serializers import UserFavSerializer, UserFavListSerializer, UserLeavingMessageSerializer, \
    UserAddressSerializer
from utils.permissions import IsOwnerOrReadOnly


# Create your views here.
class UserFavViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                     mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    # queryset = UserFav.objects.all()
    # serializer_class = UserFavSerializer
    # 需要返回的是产品id不是pk
    lookup_field = 'goods_id'
    # 认证
    # 一般都不会配置全局配置，token过期或不过期,都允许查看某些资源
    # 需要局部添加认证信息
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    # 权限
    # 只允许经过身份验证的用户访问。
    # 允许访问对象级权限，只允许对象的所有者编辑它。
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        """
        获取当前用户的查询集
        :return:
        """
        return UserFav.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        '''
        动态的配置序列化，根据list与其他操作配置，序列化UserFavListSerializer，UserFavSerializer
        :return:
        '''
        if self.action == 'list':
            return UserFavListSerializer
        else:
            return UserFavSerializer


class UserLeavingMessageViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
                                viewsets.GenericViewSet):
    # 认证
    # 一般都不会配置全局配置，token过期或不过期,都允许查看某些资源
    # 需要局部添加认证信息
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    # 权限
    # 只允许经过身份验证的用户访问。
    # 允许访问对象级权限，只允许对象的所有者编辑它。
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = UserLeavingMessageSerializer

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class UserAddressViewSet(viewsets.ModelViewSet):
    serializer_class = UserAddressSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
