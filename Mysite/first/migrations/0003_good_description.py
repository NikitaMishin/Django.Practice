# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-24 11:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0002_auto_20170324_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='good',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
