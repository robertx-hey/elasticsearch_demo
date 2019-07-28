# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-05-22 09:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='All_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=125, verbose_name='标题')),
                ('tags', models.CharField(max_length=32, verbose_name='标签')),
                ('url', models.URLField(verbose_name='url')),
                ('img_url', models.URLField(verbose_name='图片url')),
                ('summary', models.CharField(max_length=512, verbose_name='简介')),
            ],
        ),
    ]