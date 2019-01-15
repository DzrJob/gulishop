import xadmin
from .models import *
from xadmin import views


# Create your models here.

# 主题
class BaseXadminSetting(object):
    # 主题开关
    enable_themes = True
    # 使用内部主题
    use_bootswatch = True


# 标题头尾
class CommXadminSetting(object):
    site_title = '谷粒商城后台管理系统'
    site_footer = '尚硅谷教育出品'
    # 折叠菜单
    menu_style = 'accordion'


# 商品类别信息
class GoodsCategoryAdmin(object):
    list_display = ['name', 'category_type', 'code', 'parent_category', 'is_tab', 'add_time']


# 商品信息
class GoodsAdmin(object):
    list_display = ['category', 'name', 'goods_sn', 'goods_front_image', 'click_num', 'add_time']
    # desc应用富文本
    style_fields = ['desc', 'ueditor']


# 赞助信息
class CategoryBrandAdmin(object):
    list_display = ['category', 'image', 'name', 'add_time']


# 商品轮播图信息
class GoodsImageAdmin(object):
    list_display = ['goods', 'image', 'add_time']


# 首页轮播图信息
class BannerAdmin(object):
    list_display = ['goods', 'image', 'index', 'add_time']


# 注册到后台管理
xadmin.site.register(GoodsCategory, GoodsCategoryAdmin)
xadmin.site.register(Goods, GoodsAdmin)
xadmin.site.register(CategoryBrand, CategoryBrandAdmin)
xadmin.site.register(GoodsImage, GoodsImageAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseXadminSetting)
xadmin.site.register(views.CommAdminView, CommXadminSetting)
