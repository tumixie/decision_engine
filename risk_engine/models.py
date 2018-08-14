# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Rule(models.Model):
    rule_name = models.CharField(max_length=10)
    rule_body = models.TextField()
    rule_des = models.TextField()
    rule_pkg = models.CharField(max_length=20, null=True)
    rule_flow_group = models.ForeignKey('RuleGroup', null=True)
    rule_policy = models.ManyToManyField('Policy')
    create_time = models.DateTimeField()
    version = models.CharField(max_length=15)

    def __str__(self):
        return self.rule_name

    class Meta(object):
        ordering = ['rule_name']


class RuleGroup(models.Model):
    rule_group_name = models.CharField(max_length=10)
    rule_group_body = models.TextField()
    rule_group_des = models.TextField()
    rule_group_pkg = models.CharField(max_length=20)
    rule_group_policy = models.ManyToManyField('Policy')
    create_time = models.DateTimeField()
    version = models.CharField(max_length=15)

    def __str__(self):
        return self.rule_group_name

    class Meta(object):
        ordering = ['rule_group_name']


class Policy(models.Model):
    policy_name = models.CharField(max_length=25)
    k_session_type = models.CharField(max_length=10)
    k_session_name = models.CharField(max_length=50)
    create_time = models.DateTimeField()
    product = models.CharField(max_length=20, null=True)
    version = models.CharField(max_length=15)

    def __str__(self):
        return self.policy_name

    class Meta(object):
        ordering = ['policy_name']
