# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

import requests
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt

from utils import raw_data, brms_parser
from . import models

# Create your views here.


@login_required
def index(request):
    return HttpResponse(render(request, 'base.html'))


@login_required
def row_keys(request, apply_no=None):
    if apply_no is None and request.method == 'POST':
        apply_no = request.POST.get('apply_no')
    if apply_no is not None:
        return HttpResponseRedirect(reverse('row_keys_detail', kwargs={'apply_no': apply_no}))
    return HttpResponse(render(request, 'raw_data.html'))


@login_required
def row_keys_detail(request, apply_no=None):
    context = dict()
    row_key_lst = raw_data.get_row_keys(apply_no)
    if len(row_key_lst) == 0:
        context['row_keys_empty'] = True
    context['row_keys'] = row_key_lst
    return HttpResponse(render(request, 'raw_data.html', context))


@login_required
def raw_data_detail(request, row_key):
    if 'dm' in row_key:
        table = 'kafka_bd_trigger_dm'
    elif 'bom' in row_key:
        table = 'kafka_bd_trigger_bom'
    else:
        raise ValueError("非法rowkey")
    obj = raw_data.get_raw_data(table, row_key)
    return HttpResponse(obj, content_type='application/json')


@login_required
def work_flow(request):
    context = dict()
    if request.method == 'POST':
        apply_no = request.POST.get('apply_no')
        process_id = request.POST.get('process_id')
        if apply_no is not None:
            return HttpResponseRedirect(reverse('work_flow_detail_by_apply_no', kwargs={'apply_no': apply_no}))
        elif process_id is not None:
            return HttpResponseRedirect(reverse('work_flow_detail_by_process_id', kwargs={'process_id': process_id}))
    return HttpResponse(render(request, 'work_flow.html', context=context))


@login_required
def work_flow_detail_by_apply_no(request, apply_no):
    url = "http://ndesapi.quarkfinance.com/ndes/workflow/state/findByLoanNo/{apply_no}"
    return HttpResponse(requests.get(url.format(apply_no=apply_no)), content_type='application/json')


@login_required
def work_flow_detail_by_process_id(request, process_id):
    url = "http://ndesapi.quarkfinance.com/ndes/workflow/state/findByProcessId/{process_id}"
    return HttpResponse(requests.get(url.format(process_id=process_id)), content_type='application/json')


@login_required
def brms(request):
    products = models.Product.objects.all()
    context = {'products': products}
    return HttpResponse(render(request, 'brms.html', context=context))


class BrmsDetailRule(ListView):
    model = models.Rule
    template_name = 'brms.html'
    paginate_by = 12

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = len(self.object_list) == 0
            if is_empty:
                raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_queryset(self):
        queryset = models.Rule.objects
        if self.request.method == 'POST':
            policy = self.request.POST.get('policy')
            product = self.request.POST.get('product')
            version = self.request.POST.get('version')
            rule = self.request.POST.get('rule')
            valid_start_date = self.request.POST.get('valid_start_date')
            valid_end_date = self.request.POST.get('valid_end_date')
            if policy is not None and len(policy) != 0:
                queryset = queryset.filter(rule_policy__policy_name__contains=policy)
            if product is not None and len(product) != 0:
                queryset = queryset.filter(rule_policy__product__product_name=product)
            if version is not None:
                queryset = queryset.filter(version__contains=version)
            if rule is not None and len(rule) != 0:
                queryset = queryset.filter(rule_name=rule)
            if valid_start_date is not None and len(valid_start_date) != 0:
                queryset = queryset.filter(create_time__gte=datetime.strptime(valid_start_date, '%Y-%m-%d %H:%M:%S'))
            if valid_end_date is not None and len(valid_end_date) != 0:
                queryset = queryset.filter(create_time__lte=datetime.strptime(valid_end_date, '%Y-%m-%d %H:%M:%S'))
        return queryset.distinct().all()

    def get_context_data(self, **kwargs):
        context = super(BrmsDetailRule, self).get_context_data(**kwargs)
        context['products'] = models.Product.objects.all()
        return context

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(BrmsDetailRule, self).dispatch(*args, **kwargs)


class BrmsDetailRuleGroup(ListView):
    model = models.RuleGroup
    template_name = 'brms.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(BrmsDetailRuleGroup, self).get_context_data(**kwargs)
        context['products'] = models.Product.objects.all()
        return context

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(BrmsDetailRuleGroup, self).dispatch(*args, **kwargs)


def brms_detail_rule_by_id(request, id):
    context = {'rule_body': models.Rule.objects.get(id=id).rule_body}
    return HttpResponse(render(request, 'rule_body.html', context))


def brms_detail_rule_group_by_id(request, id):
    context = {'rule_body': models.RuleGroup.objects.get(id=id).rule_group_body}
    return HttpResponse(render(request, 'rule_body.html', context))


def brms_util(request):
    context = dict()
    if request.method == 'GET':
        return HttpResponse(render(request, 'brms_util.html'))
    elif request.method == 'POST':
        version = request.POST.get('version')
        filepath = request.POST.get('addr')
        if version is not None and filepath is not None:
            rule_files = brms_parser.list_rule_files(filepath)
            rule_group_files = brms_parser.list_rule_group_files(filepath)
            k_module_file = brms_parser.get_kmodule_setting_file(filepath)
            for rule_group_file in rule_group_files:
                brms_parser.detail_rule_group_parser(rule_group_file, version=version)
            for ii, rule_file in enumerate(rule_files):
                brms_parser.detail_rule_parser(rule_file, version=version)
            brms_parser.detail_policy_parser(k_module_file, version=version)
            context['status'] = 'ok'
        return HttpResponse(render(request, 'brms_util.html', context=context))


