# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-11-15 14:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visualRef', '0004_star_star_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='star',
            name='star_source',
            field=models.CharField(default='Unknown', max_length=100),
            preserve_default=False,
        ),
    ]
