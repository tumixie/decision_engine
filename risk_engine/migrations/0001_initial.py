# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-13 08:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policy_name', models.CharField(max_length=25)),
                ('k_session_type', models.CharField(max_length=10)),
                ('k_session_name', models.CharField(max_length=50)),
                ('rule_pkg', models.CharField(max_length=30)),
                ('create_time', models.DateTimeField()),
                ('version', models.CharField(max_length=15)),
            ],
            options={
                'ordering': ['policy_name'],
            },
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule_name', models.CharField(max_length=10)),
                ('rule_body', models.TextField()),
                ('rule_des', models.TextField()),
                ('rule_pkg', models.CharField(max_length=20, null=True)),
                ('create_time', models.DateTimeField()),
                ('version', models.CharField(max_length=15)),
                ('policy', models.ManyToManyField(to='risk_engine.Policy')),
            ],
            options={
                'ordering': ['rule_name'],
            },
        ),
        migrations.CreateModel(
            name='RuleGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule_group_name', models.CharField(max_length=10)),
                ('rule_group_body', models.TextField()),
                ('rule_group_des', models.TextField()),
                ('create_time', models.DateTimeField()),
                ('version', models.CharField(max_length=15)),
                ('rule_group_pkg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='risk_engine.Policy')),
            ],
            options={
                'ordering': ['rule_group_name'],
            },
        ),
    ]
