# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-21 06:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mall', '0003_auto_20181021_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usera',
            name='phone',
            field=models.CharField(default='未设置', max_length=11, verbose_name='用户电话'),
        ),
    ]
