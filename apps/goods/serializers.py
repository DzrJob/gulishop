# -*-coding:utf-8-*-
from django.db.models import Q

__author__ = 'Dzr'
from goods.models import Goods, GoodsCategory, GoodsImage, Banner, CategoryBrand
from rest_framework import serializers


# 序列化器配置
# class GoodsSerializer(serializers.Serializer):
#     name = serializers.CharField(required=True)
#     shop_price = serializers.FloatField(required=True)
#     goods_front_image = serializers.ImageField(required=True)
class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        # 可以部分序列化
        # fields = ['name','add_time']
        # 可以全部序列化
        fields = '__all__'


class GoodsSerializer(serializers.ModelSerializer):
    images = GoodsImageSerializer(many=True)

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


# 首页轮播图
class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class CategoryBrandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryBrand
        fields = '__all__'


# 首页商品分类显示
class IndexCategorySerializer(serializers.ModelSerializer):
    # 显示的二级分类
    sub_cat = CategorySerializer2(many=True)
    # 赞助商
    brands = CategoryBrandsSerializer(many=True)
    # 自己定义方法获取一级类别商品
    goods = serializers.SerializerMethodField()
    # 自定义方法获得广告
    ad_goods = serializers.SerializerMethodField()

    def get_goods(self, obj):
        """
        拿到一级类别下的所有商品
        :param obj: 序列化的那个一级类别
        :return: 自己序列化的数据
        """
        all_goods = Goods.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id) | Q(
            category__parent_category__parent_category_id=obj.id))
        serializers = GoodsSerializer(all_goods,many=True)
        return serializers.data

    def get_ad_goods(self,obj):
        ad_goods = Goods.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id) | Q(
            category__parent_category__parent_category_id=obj.id))[0]
        serializers = GoodsSerializer(ad_goods, many=False)
        return serializers.data

    class Meta:
        model = GoodsCategory
        fields = '__all__'
