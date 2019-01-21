"""gulishop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
# token认证
from rest_framework.authtoken import views
# jwt认证
from rest_framework_jwt.views import obtain_jwt_token
import xadmin
# 引入静态文件的serve
from django.views.static import serve
# 导入工程配置文件中的MEDIA_ROOT
from gulishop.settings import MEDIA_ROOT
# from apps.goods.views import GoodsView
from apps.goods.views import GoodsViewSet, CategoryViewSet
from apps.users.views import VerifyCodeViewSet, UserViewSet
from rest_framework import routers
from operations.views import UserFavViewSet,UserLeavingMessageViewSet,UserAddressViewSet

"""
# 创建默认的router对象，并注册视图集
# 与SimpleRouter的区别，DefaultRouter会多附带一个默认的API根视图，返回一个包含所有列表视图的超链接响应数据。
# register(prefix, viewset, base_name)
# prefix 该视图集的路由前缀
# viewset 视图集
# base_name 路由名称的前缀
"""
router = routers.DefaultRouter()
router.register(r'goods', GoodsViewSet, base_name='goods')
router.register(r'categorys', CategoryViewSet, base_name='categorys')
router.register(r'code', VerifyCodeViewSet, base_name='code')
router.register(r'users', UserViewSet, base_name='users')
router.register(r'userfavs',UserFavViewSet,base_name='userfavs')
router.register(r'messages',UserLeavingMessageViewSet,base_name='messages')
router.register(r'address',UserAddressViewSet,base_name='address')


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    # 该url专门处理媒体文件media路径访问
    url(r'^media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),
    # 配置富文本器
    url(r'^ueditor/', include('DjangoUeditor.urls')),

    # 配置 rest_framework
    url(r'^api-auth/', include('rest_framework.urls')),

    # 配置 接口的路由
    # url(r'^goods/$',GoodsView.as_view()),

    # 绑定 接口的请求方法（接口中可以不写get方法了）
    # url(r'^goods/$', GoodsViewSet.as_view({'get': 'list'})),
    # 添加路由数据方式一
    # url(r'^', include(router.urls))

    # 是token认证的登陆方式
    # url(r'^login/', views.obtain_auth_token),
    # JWTtoken认证的登陆方式
    url(r'^login/', obtain_jwt_token),
]
# 添加路由数据方式二
urlpatterns += router.urls
