from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from trade.serializers import ShoppingCartSerializer, ShoppingCartListSerializer
from .models import ShopCart


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

        goods = serializer.validated_data['goods']
        nums = serializer.validated_data['nums']

        shopcart_list = ShopCart.objects.filter(user=self.request.user, goods=goods)
        # 是否存在相同产品
        if shopcart_list:
            shopcart = shopcart_list[0]
            shopcart.nums += nums
            shopcart.save()
        else:
            shopcart = ShopCart()
            shopcart.user = self.request.user
            shopcart.goods = goods
            shopcart.nums = nums
            shopcart.save()

        # 不重写返回的是原来的序列化数据，因为是新的数据，需要重新读取序列化
        serializer = self.get_serializer_class()(shopcart)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
