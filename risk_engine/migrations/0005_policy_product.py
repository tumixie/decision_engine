# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-14 03:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('risk_engine', '0004_rule_rule_flow_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='policy',
            name='product',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
