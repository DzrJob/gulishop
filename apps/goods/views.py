from rest_framework.response import Response

from goods.models import Goods, GoodsCategory, Banner
from goods.filters import GoodsFilter
from goods.paginations import GoodsPagination
from goods.serializers import GoodsSerializer, CategorySerializer, BannerSerializer

# 导入rest_framework
from rest_framework import mixins, generics, pagination, filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend

# 首页轮播图
class BannerViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    queryset = Banner.objects.all().order_by('-index')
    serializer_class = BannerSerializer

# 商品分类接口
class CategoryViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


"""使用rest_framework GenericAPIView扩展类GenericViewSet与mixins组合 实现接口"""
class GoodsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    # 必要的查询集
    queryset = Goods.objects.all()
    # 过滤配置（区间，搜索，排序）
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # 序列化配置
    serializer_class = GoodsSerializer
    # 分页配置
    pagination_class = GoodsPagination
    # 用于区间功能的字段
    filter_class = GoodsFilter
    # 用于搜索功能的字段
    search_fields = ('name',)
    # 用于排序的字段
    ordering_fields = ('shop_price',)
    # get post delete put 等方法放在路由当中去做绑定

    # 每次点击产品详情为该商品添加访问量，需要重写方法
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


"""使用rest_framework APIView扩展类GenericAPIView与mixins组合 实现接口"""
# class GoodsView(mixins.ListModelMixin, generics.GenericAPIView):
#     # 必要的查询集
#     queryset = Goods.objects.all()
#     # 过滤配置（区间，搜索，排序）
#     filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
#     # 序列化配置
#     serializer_class = GoodsSerializer
#     # 分页配置
#     pagination_class = GoodsPagination
#
#     # filter_fields = ('name',)
#     # 用于区间功能的字段
#     filter_class = GoodsFilter
#     # 用于搜索功能的字段
#     search_fields = ('name',)
#     # 用于排序的字段
#     ordering_fields = ('shop_price',)
#     # get请求处理
#     def get(self, request, *args, **kwargs):
#         # 组合使用 mixins.ListModelMixin generics.GenericAPIView
#         # list()展示所有数据的核心方法
#         return self.list(request, *args, **kwargs)

"""使用rest_framework View扩展类APIView 实现接口"""
# from rest_framework.views import APIView
# from .serializers import GoodsSerializer
# from rest_framework.response import Response
# class GoodsView(APIView):
# # 使用drf最基础的APIview实现商品列表的数据接口
#     def get(self,request):
#         all_goods = Goods.objects.all()
#         serializer = GoodsSerializer(all_goods,many=True)
#         return Response(data=serializer.data)


"""使用原生 View 实现接口"""
# import json
# from django.views import View
# from django.shortcuts import render, HttpResponse
# from django.http import JsonResponse
# from django.core import serializers
# from django.forms import model_to_dict

# class GoodsView(View):
# # 第一种方式，python自带序列化，序列化不方便，不支持图片序列化json
# def get(self, request):
# queryset
#     all_goods = Goods.objects.all()
#     # 第一种序列化
#     items = []
#     for goods in all_goods:
# query对象转字典
#         item = {}
#         item['name'] = goods.name
#         item['shop_price'] = goods.shop_price
#         # TypeError at /goods/   Object of type 'ImageFieldFile' is not JSON serializable
#         # item['goods_front_image'] = goods.goods_front_image
#         items.append(item)
#     # 使用HttpResponse返回需要先去把python的json格式类型转化为json的字符串
#     # data = json.dumps(items)
#     # return HttpResponse(data,content_type='application/json')
#     return JsonResponse(items, safe=False)


# # 第二种方式,django自带model_to_dict，全部序列化，不支持图片序列化json
# def get(self, request):
#     all_goods = Goods.objects.all()
#     items = []
#     for goods in all_goods:
#         item = model_to_dict(goods)
#         items.append(item)
#     # 使用HttpResponse返回需要先去把python的json格式类型转化为json的字符串
#     # data = json.dumps(items)
#     # return HttpResponse(data, content_type='application/json')
#     return JsonResponse(items, safe=False)


# # 第三种方式，django自带serializers，支持图片序列化json
# def get(self, request):
#     all_goods = Goods.objects.all()
#     data = serializers.serialize('json', all_goods)
#     # data = json.loads(data)
#     # return JsonResponse(data, safe=False)
#     return HttpResponse(data, content_type='application/json')
