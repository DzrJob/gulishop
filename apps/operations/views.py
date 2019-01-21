from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, viewsets

from operations.models import UserFav
from operations.serializers import UserFavSerializer


class UserFavViewSet(mixins.CreateModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer
    # 需要返回的是产品id不是pk
    lookup_field = 'goods_id'
