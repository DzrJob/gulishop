#-*-coding:utf-8-*-
__author__ = 'Dzr'
from goods.serializers import GoodsSerializer
from operations.models import UserFav, UserLeavingMessage
from rest_framework import serializers


class UserFavSerializer(serializers.ModelSerializer):
    # browserAPI中可以更改收藏者，需要设置成当前用户，并且隐藏
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # 把添加时间格式化成更高可读性
    add_time = serializers.DateTimeField(read_only=True,format='%Y-%m-%d %H-%M-%S')

    class Meta:
        model = UserFav
        fields = '__all__'


class UserFavListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True,format="%Y-%m-%d %H:%M:%S")
    # goods是userfav表中外键字段，对应一个商品，所以序列化的时候many=False
    # 通过related_name的值，获取到的是所有的子表对象，然后去序列化，因此many=True
    goods = GoodsSerializer(many=False)
    class Meta:
        model = UserFav
        fields = '__all__'


class UserLeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = UserLeavingMessage
        fields = '__all__'