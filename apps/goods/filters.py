# -*-coding:utf-8-*-
__author__ = 'Dzr'
from django_filters import rest_framework as filters
from goods.models import Goods

# 区间过滤配置
class GoodsFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='shop_price', lookup_expr='gte', label='最低价格')
    max_price = filters.NumberFilter(field_name='shop_price', lookup_expr='lte', label='最高价格')

    class Meta:
        model = Goods
        fields = ['min_price', 'max_price']
