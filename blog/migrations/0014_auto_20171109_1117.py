# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-09 05:47
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20171109_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='date_published',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 11, 9, 5, 47, 49, 953053, tzinfo=utc), null=True, verbose_name='Date article published'),
        ),
    ]
