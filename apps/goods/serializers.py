# -*-coding:utf-8-*-
__author__ = 'Dzr'
from goods.models import Goods, GoodsCategory
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

# 嵌套序列化
class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'

# 嵌套序列化
class CategorySerializer2(serializers.ModelSerializer):
    # 必须是related_name的值，才能拿到子表对象序列化
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'

# 嵌套序列化
class CategorySerializer(serializers.ModelSerializer):
    # 必须是related_name的值，才能拿到子表对象序列化
    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'
