#-*-coding:utf-8-*- 
__author__ = 'Dzr'
# 配置我们文件所在目录的搜索环境
import os,sys
# 当前文件的路径
file_path = os.path.abspath(__file__)
# 根据这个路径，找到这个文件所在目录路径
dir_path = os.path.dirname(file_path)
# D:\dev\PycharmProjects\django\gulishop\db_tools\import_category.py
# D:\dev\PycharmProjects\django\gulishop\db_tools
# print(file_path,dir_path)

# 添加路径到搜寻环境
sys.path.append(dir_path)
# 动态设置setting文件
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gulishop.settings")
# 初始化环境生效
import django
django.setup()
# 不能放在上面
from goods.models import GoodsCategory
from db_tools.data.category_data import row_data

# 遍历获取数据
for lev1 in row_data:
    # 一级类别数据
    cat1 = GoodsCategory()
    cat1.name = lev1['name']
    cat1.code = lev1['code'] if lev1['code'] else ''
    cat1.category_type = 1
    cat1.save()

    for lev2 in lev1['sub_categorys']:
        # 二级类别数据
        cat2 = GoodsCategory()
        cat2.name = lev2['name']
        cat2.code = lev2['code'] if lev2['code'] else ''
        cat2.category_type = 2
        cat2.parent_category = cat1
        cat2.save()

        for lev3 in lev2['sub_categorys']:
            # 三级类别数据
            cat3 = GoodsCategory()
            cat3.name = lev3['name']
            cat3.code = lev3['code'] if lev3['code'] else ''
            cat3.category_type = 3
            cat3.parent_category = cat2
            cat3.save()