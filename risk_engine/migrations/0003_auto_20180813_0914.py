# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-13 09:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('risk_engine', '0002_auto_20180813_0913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rule',
            name='rule_pkg',
            field=models.CharField(max_length=20, null=True),
        ),
    ]