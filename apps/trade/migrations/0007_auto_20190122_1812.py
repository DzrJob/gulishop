# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-01-22 18:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0006_auto_20190122_1809'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderinfo',
            old_name='pay_trade_status',
            new_name='pay_status',
        ),
    ]
