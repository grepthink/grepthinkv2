# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-03 18:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_auto_20170303_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectupdate',
            name='update',
            field=models.TextField(default='Default Update', max_length=2000),
        ),
        migrations.AlterField(
            model_name='projectupdate',
            name='update_title',
            field=models.CharField(default='Default Update Title', max_length=255),
        ),
    ]
