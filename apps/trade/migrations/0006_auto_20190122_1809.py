# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-01-22 18:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0005_auto_20190122_1808'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ordergoods',
            old_name='goods_nums',
            new_name='goods_num',
        ),
    ]
