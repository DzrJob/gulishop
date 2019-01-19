from django.db import models
from datetime import  datetime
# Create your models here.
from DjangoUeditor.models import UEditorField


class GoodsCategory(models.Model):
    name = models.CharField(max_length=20,verbose_name="商品类别名称")
    category_type = models.IntegerField(choices=((1,'一级'),(2,'二级'),(3,'三级')),verbose_name='类别级别')
    code = models.CharField(max_length=50,verbose_name="类别编号")
    parent_category = models.ForeignKey('self',verbose_name="所属上级类别",null=True,blank=True,related_name='sub_cat')
    is_tab = models.BooleanField(default=False,verbose_name="是否导航")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '商品类别信息'
        verbose_name_plural = verbose_name


class Goods(models.Model):
    category = models.ForeignKey(GoodsCategory,verbose_name="所属类别",related_name='goods')
    name = models.CharField(max_length=100,verbose_name="商品名称")
    goods_sn = models.CharField(max_length=30,verbose_name="商品唯一编号",unique=True,null=True,blank=True)
    goods_brief = models.CharField(max_length=300,verbose_name="商品简介",null=True,blank=True)
    goods_desc = UEditorField(verbose_name='商品详情',
                        width=900,
                        height=400,
                        toolbars='full',
                        imagePath='ueditor/images/',
                        filePath='ueditor/files/',
                        upload_settings={'imageMaxSizing': 1024000},
                        default='')

    goods_front_image = models.ImageField(upload_to='goods/images',max_length=200,verbose_name="商品封面图")
    market_price = models.FloatField(verbose_name="商品市场价")
    shop_price = models.FloatField(verbose_name='商品店铺价')
    ship_free = models.BooleanField(default=True,verbose_name="是否包邮")
    click_num = models.IntegerField(default=0,verbose_name="商品访问量")
    fav_num = models.IntegerField(default=0,verbose_name="商品收藏数")
    goods_num = models.IntegerField(default=100,verbose_name="商品库存数")
    sold_num = models.IntegerField(default=0,verbose_name="商品销售数")
    is_hot = models.BooleanField(default=False,verbose_name='是否热卖')
    is_new = models.BooleanField(default=False,verbose_name="是否新品")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = verbose_name


class CategoryBrand(models.Model):
    category = models.ForeignKey(GoodsCategory,verbose_name="所属类别",related_name='brands')
    image=  models.ImageField(upload_to='brand/images',verbose_name="赞助图片",max_length=200)
    name = models.CharField(max_length=30,verbose_name="赞助名称")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '赞助信息'
        verbose_name_plural = verbose_name



class GoodsImage(models.Model):
    goods = models.ForeignKey(Goods,verbose_name="所属商品",related_name='images')
    image = models.ImageField(upload_to='goods/images',verbose_name="商品轮播图片",max_length=200)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.goods.name

    class Meta:
        verbose_name = '商品轮播图信息'
        verbose_name_plural = verbose_name


class Banner(models.Model):
    goods = models.ForeignKey(Goods, verbose_name="所属商品", related_name='banners')
    image = models.ImageField(upload_to='goods/images', verbose_name="首页轮播图片", max_length=200)
    index = models.IntegerField(verbose_name="轮播顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.goods.name

    class Meta:
        verbose_name = '首页轮播图信息'
        verbose_name_plural = verbose_name