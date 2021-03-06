#-*-coding:utf-8-*-
from rest_framework import pagination

__author__ = 'Dzr'

# 分页器配置
class GoodsPagination(pagination.PageNumberPagination):
    # 每页数据（根据前端参数配置属性名）
    page_size = 12
    # 页码 路径参数
    page_query_param = 'page'
    # 每页数据 路径参数
    page_size_query_param = 'page_size'
    # 每页最大 数据
    # max_page_size = 10