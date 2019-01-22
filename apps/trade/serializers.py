# -*-coding:utf-8-*-
__author__ = 'Dzr'
from rest_framework import serializers
from .models import ShopCart, OrderInfo, OrderGoods
from goods.serializers import GoodsSerializer


class ShoppingCartSerializer(serializers.ModelSerializer):
    # browserAPI中可以更改收藏者，需要设置成当前用户，并且隐藏
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # 把添加时间格式化成更高可读性
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H-%M-%S')

    class Meta:
        model = ShopCart
        fields = '__all__'


class ShoppingCartListSerializer(serializers.ModelSerializer):
    # browserAPI中可以更改收藏者，需要设置成当前用户，并且隐藏
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # 把添加时间格式化成更高可读性
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H-%M-%S')

    # 通过related_name的值，获取到的是所有的子表对象，然后去序列化，因此many=True
    goods = GoodsSerializer(many=False)

    class Meta:
        model = ShopCart
        fields = '__all__'


class OrderInfoSerializer(serializers.ModelSerializer):
    # browserAPI中可以更改收藏者，需要设置成当前用户，并且隐藏
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # 把添加时间格式化成更高可读性
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H-%M-%S')
    order_sn = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    pay_trade_status = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = OrderInfo
        fields = '__all__'


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = '__all__'


class OrderInfoDetailsSerializer(serializers.ModelSerializer):
    # browserAPI中可以更改收藏者，需要设置成当前用户，并且隐藏
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # 把添加时间格式化成更高可读性
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H-%M-%S')

    goods = OrderGoodsSerializer(many=True)

    class Meta:
        model = OrderInfo
        fields = '__all__'
