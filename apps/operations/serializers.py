#-*-coding:utf-8-*-
__author__ = 'Dzr'
from operations.models import UserFav
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