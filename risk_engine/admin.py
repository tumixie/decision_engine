# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from . import models

# Register your models here.


class RuleAdmin(admin.ModelAdmin):
    # ...
    list_display = ('rule_name', 'rule_pkg', 'rule_flow_group', 'create_time',
                    'version')
    list_filter = ['rule_pkg']  # 添加过滤条件
    # search_fields = ['question_text']  # 添加搜索条件，后台数据库实现用like

admin.site.register(models.Rule, RuleAdmin)
admin.site.register(models.Policy)
admin.site.register(models.RuleGroup)
admin.site.register(models.Product)


