from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
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
            order_goods.save()

        # 第三步：清空购物车
        cart_list.delete()
        # 重新读取serializer
        serializer = self.get_serializer(order)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # 获得唯一订单号方法
    def get_order_sn(self):
        order_sn = '{date_now}{user_id}{random}'.format(date_now=str(time.strftime('%Y%m%d%H%M%S')),
                                                        user_id=str(self.request.user.id),
                                                        random=str(random.randint(10, 99)))
        return order_sn
