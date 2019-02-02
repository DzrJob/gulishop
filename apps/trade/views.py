from datetime import datetime

from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

from gulishop.settings import app_id, private_key, ali_key
from utils.Alipay import AliPay
from utils.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from trade.serializers import ShoppingCartSerializer, ShoppingCartListSerializer, OrderInfoSerializer, \
    OrderInfoDetailsSerializer
from .models import ShopCart, OrderInfo, OrderGoods
import time
import random


# Create your views here.

class ShoppingCartViewSet(viewsets.ModelViewSet):
    # queryset = ShopCart.objects.all()
    # serializer_class = ShoppingCartSerializer

    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    lookup_field = 'goods_id'

    def get_queryset(self):
        return ShopCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ShoppingCartListSerializer
        else:
            return ShoppingCartSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 从serializer中读取传入的值
        goods = serializer.validated_data['goods']
        nums = serializer.validated_data['nums']
        # 根据当前用户，与传入的商品过滤，得到查询集
        shopcart_list = ShopCart.objects.filter(user=self.request.user, goods=goods)
        # 判断是否存在该查询集
        if shopcart_list:
            # 该查询集存在，改变商品数量
            shopcart = shopcart_list[0]
            shopcart.nums += nums
            shopcart.save()
        else:
            # 不存在，创建该对象
            shopcart = ShopCart()
            shopcart.user = self.request.user
            shopcart.goods = goods
            shopcart.nums = nums
            shopcart.save()

        # 不重写返回的是原来的序列化数据，因为是新的数据，需要重新读取序列化
        # serializer = self.get_serializer_class()(shopcart)
        serializer = self.get_serializer(shopcart)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class OrderInfoViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                       mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderInfoDetailsSerializer
        else:
            return OrderInfoSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        alipay = AliPay(
            appid=app_id,
            app_notify_url='http://127.0.0.1:8000/alipay_return/',
            app_private_key_path=private_key,
            alipay_public_key_path=ali_key,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url='http://127.0.0.1:8000/alipay_return/'
        )
        url = alipay.direct_pay(
            subject=instance.order_sn,
            out_trade_no=instance.order_sn,
            total_amount=instance.order_mount
        )
        # 沙箱环境
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        serializer = self.get_serializer(instance)
        ret = serializer.data
        ret['alipay_url'] = re_url
        return Response(ret)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 第一步：创建订单
        order = OrderInfo.objects.create(**serializer.validated_data)
        order.order_sn = self.get_order_sn()
        order.save()

        # 第二步：创建好订单的订单商品并且与订单进行关联
        cart_list = ShopCart.objects.filter(user=self.request.user)
        for cart in cart_list:
            order_goods = OrderGoods()
            order_goods.order = order
            order_goods.goods = cart.goods
            order_goods.goods_num = cart.nums
            # 订单创建后，商品库存量-1
            order_goods.goods.goods_num -= cart.nums
            order_goods.goods.save()
            order_goods.save()

        # 第三步：清空购物车
        cart_list.delete()

        # 第四步：生成订单支付链接，加入我们的返回数据当中，为了让前端可以去请求这个支付页面
        alipay = AliPay(
            appid=app_id,
            app_notify_url='http://127.0.0.1:8000/alipay_return/',
            app_private_key_path=private_key,
            alipay_public_key_path=ali_key,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url='http://127.0.0.1:8000/alipay_return/'
        )
        url = alipay.direct_pay(
            subject=order.order_sn,
            out_trade_no=order.order_sn,
            total_amount=order.order_mount
        )

        # 沙箱环境
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        # 重新读取serializer
        serializer = self.get_serializer(order)
        ret = serializer.data
        ret['alipay_url'] = re_url
        headers = self.get_success_headers(serializer.data)
        return Response(ret, status=status.HTTP_201_CREATED, headers=headers)

    # 获得唯一订单号方法
    def get_order_sn(self):
        order_sn = '{date_now}{user_id}{random}'.format(date_now=str(time.strftime('%Y%m%d%H%M%S')),
                                                        user_id=str(self.request.user.id),
                                                        random=str(random.randint(10, 99)))
        return order_sn


class AliPayView(APIView):

    def post(self, request):
        """
        处理支付宝的notify_url
        """
        # 1. 先将sign剔除掉
        data_dict = {}  # 接收支付宝传递参数
        for key, value in request.POST.items():  # 循环参数
            data_dict[key] = value  # 将参数添加到字典
        sign = data_dict.pop("sign", None)  # 单独拿出sign字段
        # 2. 生成一个Alipay对象
        alipay = AliPay(  # 传递参数初始化支付类
            appid="",  # 设置签约的appid
            app_notify_url="http://127.0.0.1:8000/alipay_return/",  # 异步支付通知url
            app_private_key_path=private_key,  # 设置应用私钥
            alipay_public_key_path=ali_key,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 设置是否是沙箱环境，True是沙箱环境 默认False,
            return_url="http://127.0.0.1:8000/alipay_return/"  # 同步支付通知url，跳转地址
        )
        # 3. 进行验签，确保这是支付宝给我们的
        result = alipay.verify(data_dict, sign)
        if result:
            order_sn = data_dict.get('out_trade_no', '')
            trade_no = data_dict.get('trade_no', '')
            pay_time = datetime.now()
            pay_status = data_dict.get('trade_status', 'TRADE_SUCCESS')

            order_list = OrderInfo.objects.filter(order_sn=order_sn)
            if order_list:
                order = order_list[0]
                order.pay_status = pay_status
                order.pay_time = pay_time
                order.trade_no = trade_no
                order.save()
                # 订单完成 为所有订单商品 添加订单商品数量的销售量
                order_goods_list = order.goods.all()
                for order_goods in order_goods_list:
                    order_goods.goods.sold_num += order_goods.goods_num
                    order_goods.save()
                # 将success返回给支付宝，支付宝就不会一直不停的继续发消息了。
                return Response('success')

    def get(self, request):
        """
        处理支付宝的return_url返回
        """
        data_dict = {}
        # 1. 获取GET中参数
        for key, value in request.GET.items():
            data_dict[key] = value
        # 2. 取出sign
        sign = data_dict.pop("sign", None)
        # 3. 生成ALipay对象
        alipay = AliPay(
            appid=app_id,
            app_notify_url="http://127.0.0.1:8080",
            app_private_key_path=private_key,
            alipay_public_key_path=ali_key,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://127.0.0.1:8080"
        )
        result = alipay.verify(data_dict, sign)
        # 这里可以不做操作。因为不管发不发return url。notify url都会修改订单状态。
        if result:
            order_sn = data_dict.get('out_trade_no', '')
            trade_no = data_dict.get('trade_no', '')
            pay_time = datetime.now()
            pay_status = data_dict.get('trade_status', 'TRADE_SUCCESS')

            order_list = OrderInfo.objects.filter(order_sn=order_sn)
            if order_list:
                order = order_list[0]
                order.pay_status = pay_status
                order.pay_time = pay_time
                order.trade_no = trade_no
                order.save()
                from django.shortcuts import redirect, reverse
                ret = redirect(reverse('index'))
                # ret = redirect('http://127.0.0.1:8080')
                # 可以直接去到订单列表页
                ret.set_cookie('nextPath', 'pay', 2)
                return ret
