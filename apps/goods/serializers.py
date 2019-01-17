# -*-coding:utf-8-*-
__author__ = 'Dzr'
from goods.models import Goods
from rest_framework import serializers

# 序列化器配置
# class GoodsSerializer(serializers.Serializer):
#     name = serializers.CharField(required=True)
#     shop_price = serializers.FloatField(required=True)
#     goods_front_image = serializers.ImageField(required=True)

class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        # 指定model中要验证的类
        model = Goods
        # 指定序列化
        # fields = ['name','goods_front_image']
        # 全部序列化
        fields = '__all__'
