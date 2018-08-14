# coding: utf-8

import json
import base64

from lxml import etree
import requests
from django.http import HttpResponse, Http404


def get_row_keys(apply_no):
    # url = "http://idc-hadoopsh-05:20550/kafka_bd_trigger_dm/trigger_dm_{apply_no}*"
    url = "http://172.16.1.185:20550/kafka_bd_trigger_dm/trigger_dm_{apply_no}*"
    response = requests.get(url.format(apply_no=apply_no))
    if response.status_code != 200:
        raise Http404
    elif response.content is None or len(response.content) == 0:
        return []
    objs = etree.HTML(response.content).xpath('//cell')
    if len(objs) == 0:
        return list()
    row_keys = list()
    dp_row_keys = set()
    for obj in objs:
        obj = json.loads(base64.decodestring(obj.text))
        row_key_templates = [
            ['kafka_bd_trigger_dm', 'trigger_dm_{apply_no}_{transaction_id}'],
            ['kafka_bd_trigger_bom', 'trigger_bom_{policy_id}_{apply_no}_{transaction_id}'],
        ]
        for row_key_template in row_key_templates:
            tp_dct = dict()
            tp_dct['policy_id'] = obj.get('policyId', '')
            tp_dct['transaction_id'] = obj.get('transactionId', '')
            tp_dct['apply_no'] = apply_no
            tp_dct['table'] = row_key_template[0]
            tp_dct['row_key'] = row_key_template[1].format(**tp_dct)
            if tp_dct['row_key'] in dp_row_keys:
                continue
            else:
                dp_row_keys.add(tp_dct['row_key'])
            row_keys.append(tp_dct)

    return row_keys


def get_raw_data(table, row_key):
    # url = "http://idc-hadoopsh-05:20550/{table}/{row_key}"
    url = "http://172.16.1.185:20550/{table}/{row_key}"  # sit
    response = requests.get(url.format(table=table, row_key=row_key))
    objs = etree.HTML(response.content).xpath('//cell')
    if len(objs) == 0:
        HttpResponse('数据不存在')
    else:
        obj = objs[0]
        return base64.decodestring(obj.text)
