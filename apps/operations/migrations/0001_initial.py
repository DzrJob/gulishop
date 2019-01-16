# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-01-16 08:36
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province', models.CharField(max_length=50, verbose_name='省')),
                ('city', models.CharField(max_length=50, verbose_name='市')),
                ('district', models.CharField(max_length=50, verbose_name='区')),
                ('signing_name', models.CharField(max_length=20, verbose_name='收货人')),
                ('signing_mobile', models.CharField(max_length=11, verbose_name='收货电话')),
                ('address', models.CharField(max_length=300, verbose_name='收货地址')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '用户收货地址信息',
                'verbose_name_plural': '用户收货地址信息',
            },
        ),
        migrations.CreateModel(
            name='UserFav',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '用户收藏信息',
                'verbose_name_plural': '用户收藏信息',
            },
        ),
        migrations.CreateModel(
            name='UserLeavingMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg_type', models.IntegerField(choices=[(1, '留言'), (2, '投诉'), (3, '询问'), (4, '售后'), (5, '求购')], default=1, verbose_name='留言类型')),
                ('subject', models.CharField(max_length=30, verbose_name='留言主题')),
                ('message', models.CharField(max_length=300, verbose_name='留言内容')),
                ('file', models.FileField(max_length=200, upload_to='users/files', verbose_name='留言文件')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '用户留言信息',
                'verbose_name_plural': '用户留言信息',
            },
        ),
    ]
