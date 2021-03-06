# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-09 03:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0019_delete_filter'),
        ('blog', '0008_blogpeoplerelationship'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogindexpage',
            name='intro',
        ),
        migrations.AddField(
            model_name='blogindexpage',
            name='image',
            field=models.ForeignKey(blank=True, help_text='Landscape mode only; horizontal width between 1000px and 3000px.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='blogindexpage',
            name='introduction',
            field=models.TextField(blank=True, help_text='Text to describe the page'),
        ),
    ]
