# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-29 00:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barrage',
            name='data',
            field=models.CharField(max_length=200),
        ),
    ]
