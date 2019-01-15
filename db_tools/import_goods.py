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
from goods.models import Goods,GoodsCategory,GoodsImage
from db_tools.data.category_data import row_data

# 遍历获取数据
for item in row_data:
    goods = Goods()
    goods.name = item['item']
    goods.goods_brief = item['desc'] if item['desc'] else ''
    goods.desc = item['goods_desc'] if item['goods_desc'] else ''
    goods.market_price = float(item['market_price'].replace('￥','').replace('元',''))
    goods.shop_price = float(item['sale_price'].replace('￥','').replace('元',''))
    goods.goods_front_image = item['images'][0] if item['images'] else ''

    # 数据中存的是类别的名字，不是类别对象，外键赋值，需要找到类别对象
    category_name = item['categorys'][-1]
    category_list = GoodsCategory.objects.filter(name=category_name)
    if category_list:
        goods.category = category_list[0]
    goods.save()

    for image in item['image']:
        goods_image = GoodsImage()
        goods_image.goods = goods
        goods_image.image = image
        goods_image.save()