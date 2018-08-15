# coding: utf-8

import os
import re
from datetime import datetime

from lxml import etree

from .. import models


def list_rule_files(d):
    """返回所有的规则文件"""
    rules = list()
    for sub_dir in os.listdir(d):
        sub_dir = os.path.join(d, sub_dir)
        if os.path.isdir(sub_dir):
            rules.extend(list_rule_files(sub_dir))
        else:
            if sub_dir.endswith('.drl'):
                rules.append(sub_dir)
            else:
                continue
    return rules


def get_kmodule_setting_file(d):
    for sub_dir in os.listdir(d):
        sub_dir = os.path.join(d, sub_dir)
        if os.path.isdir(sub_dir):
            rs = get_kmodule_setting_file(sub_dir)
            if rs is not None:
                return rs
        else:
            if sub_dir.endswith('kmodule.xml'):
                return sub_dir


def list_rule_group_files(d):
    rule_groups = list()
    for sub_dir in os.listdir(d):
        sub_dir = os.path.join(d, sub_dir)
        if os.path.isdir(sub_dir):
            rule_groups.extend(list_rule_group_files(sub_dir))
        else:
            if sub_dir.endswith('.rf'):
                rule_groups.append(sub_dir)
            else:
                continue
    return rule_groups


# def detail_rule_parser(rule_file):
#     """ 规则文件解析 """
#     rs = list()
#     rule_rule_pkg = list()
#     with open(rule_file) as f:
#         s = f.read()
#         rules = re.findall(r'rule [\s\S]*? end', s, flags=re.MULTILINE)
#         rule_package = re.search(r'package[\s]+(?P<rule_package>[a-z\.0-9]+)', s)
#         rule_package = '' if rule_package is None else rule_package.group('rule_package')
#         for rule in rules:
#             tp = dict()
#             tp_rule_rule_pkg = dict()
#             tp['rule_name'] = re.search(r"""rule ['"](?P<rule_name>.*?)['"]""", rule).group('rule_name')
#             tp['rule_body'] = rule.decode('utf-8')
#             tp['rule_des'] = ""
#             tp_rule_rule_pkg['rule_pkg'] = rule_package
#             tp['version'] = '1.1.1'
#             tp['create_time'] = datetime.now()
#             rs.append(tp)
#             rule_rule_pkg.append(tp_rule_rule_pkg)
#
#     return rs, rule_rule_pkg


def detail_rule_group_parser(rule_group_file, version):
    with open(rule_group_file) as f:
        s = f.read()
        package_name = re.search(r"""package-name=['"](?P<package_name>.*?)['"]""", s)
        if package_name is None:
            return
        else:
            package_name = package_name.group('package_name')
        rule_groups = re.findall(r"""ruleFlowGroup=['"](?P<rule_group>.*?)['"]""", s, flags=re.MULTILINE)
        for rule_group in rule_groups:
            rule_group_model = models.RuleGroup()
            rule_group_model.rule_group_name = rule_group
            rule_group_model.create_time = datetime.now()
            rule_group_model.rule_group_body = ""
            rule_group_model.rule_group_des = ""
            rule_group_model.rule_group_pkg = package_name
            rule_group_model.version = version
            rule_group_model.save()


def detail_rule_parser(rule_file, version):
    """ 规则文件解析 """
    with open(rule_file) as f:
        s = f.read()
        rules = re.findall(r'rule [\s\S]*?end', s, flags=re.MULTILINE)
        rule_package = re.search(r'package[\s]+(?P<rule_package>[a-zA-Z\_\.0-9]+)', s)
        rule_package = '' if rule_package is None else rule_package.group('rule_package')
        if rule_package == 'rules.T008':
            print rules
        for rule in rules:
            rl = models.Rule()
            rl.rule_name = re.search(r"""rule ['"](?P<rule_name>.*?)['"]""", rule).group('rule_name')
            rl.rule_body = rule.decode('utf-8')
            rl.rule_des = ""
            rl.version = version
            rl.create_time = datetime.now()
            rl.rule_pkg = rule_package
            # rl.rule_pkg.add(*models.Policy.objects.get(policy_name=rule_package, version=rl.version).all())
            rl.save()
            rule_group_name = re.search(r"""ruleflow-group ['"](?P<rule_group_name>.*?)['"]""", rule)
            if rule_group_name is not None:
                rule_group_name = rule_group_name.group('rule_group_name')
                rs = models.RuleGroup.objects.filter(version=version, rule_group_name=rule_group_name)
                if rs.count() > 0:
                    rl.rule_flow_group = rs.all()[0]
                    rl.save()


def detail_policy_parser(kmodule_setting_file, version):
    """流程配置文件解析"""
    with open(kmodule_setting_file) as f:
        text = f.read()
        obj = etree.HTML(text)
        kbases = obj.xpath('//kbase')
        for kbase in kbases:
            kbase_name = kbase.xpath('@name')[0]
            rule_pkgs = kbase.xpath('@packages')[0].replace('\n', '').replace(' ', '')
            for ksession in kbase.xpath('./ksession'):
                ksession_name = ksession.xpath('@name')[0]
                ksession_type_lst = ksession.xpath('@type')
                if len(ksession_type_lst) != 0:
                    ksession_type = ksession_type_lst[0]
                else:
                    ksession_type = ""
                if 'stateless' not in ksession_type:
                    continue
                policy = models.Policy()
                policy.policy_name = kbase_name
                product_name = u'渤海信托' if 'bh' in kbase_name else (u'暖薪贷循环额度' if 'ccl' in kbase_name else u'四只猫')
                policy.product = models.Product.objects.get(product_name=product_name)
                policy.k_session_name = ksession_name
                policy.k_session_type = ksession_type
                policy.create_time = datetime.now()
                policy.version = version
                policy.save()
            for rule_pkg in rule_pkgs.split(','):
                for rule in models.Rule.objects.filter(rule_pkg=rule_pkg, version=version).all():
                    rule.rule_policy.add(policy)
                    rule.save()
                if models.RuleGroup.objects.count() <= 0:
                    continue
                for rule_group in models.RuleGroup.objects.filter(rule_group_name=rule_pkg, version=version):
                    rule_group.rule_group_policy.add(policy)
                    rule_group.save()


# def detail_policy_parser(kmodule_setting_file):
#     """流程配置文件解析"""
#     kssesion_configs = list()
#     with open(kmodule_setting_file) as f:
#         text = f.read()
#         obj = etree.HTML(text)
#         kbases = obj.xpath('//kbase')
#         for kbase in kbases:
#             kbase_name = kbase.xpath('@name')[0]
#             rules = kbase.xpath('@packages')[0].replace('\n', '').replace(' ', '')
#             for ksession in kbase.xpath('./ksession'):
#                 ksession_name = ksession.xpath('@name')[0]
#                 ksession_type_lst = ksession.xpath('@type')
#                 if len(ksession_type_lst) != 0:
#                     ksession_type = ksession_type_lst[0]
#                 else:
#                     ksession_type = ""
#                 print rules
#                 # for rule in rules.split(','):
#                 #     tp = dict()
#                 #     tp['policy_name'] = kbase_name
#                 #     tp['k_session_name'] = ksession_name
#                 #     tp['k_session_type'] = ksession_type
#                 #     tp['rule_pkg'] = rule
#                 #     tp['create_time'] = datetime.now()
#                 #     tp['version'] = '1.1.1'
#                 #     kssesion_configs.append(tp)
#                 tp = dict()
#                 tp['policy_name'] = kbase_name
#                 tp['k_session_name'] = ksession_name
#                 tp['k_session_type'] = ksession_type
#                 tp['rule_pkg'] = ""
#                 tp['create_time'] = datetime.now()
#                 tp['version'] = '1.1.1'
#                 kssesion_configs.append(tp)
#
#     return kssesion_configs


def conn_to_mysql():
    import pymysql
    conn = pymysql.connect(host='172.30.33.82', port=3306, user='jira', passwd='jira@123', db='jira', charset='utf8')
    return conn


def fill_k_v_sql(item):
    k_sql, v_sql = '', ''
    for k, v in item.items():
        if v is not None:
            k_sql += u'`{0}`,'.format(k)
            v_sql += u"'{0}',".format(v)
    return k_sql[:-1], v_sql[:-1]


def test():
    # d = '/Users/tumixie/project/quark/ruleengine/src/main/resources/'
    d = '/Users/tumixie/project/quark/root/weijiexie/project/web/decision_engine/resources/nruleengine/src/main/resources'
    rule_files = list_rule_files(d)
    rules = list()
    rule_rule_pkg = list()
    print rule_files
    # for ii, rule_file in enumerate(rule_files):
    #     if ii > 5:
    #         break
    #     rls, pkgs_map = detail_rule_parser(rule_file)
    #     rules.extend(rls)
    #     rule_rule_pkg.extend(pkgs_map)
    # kmodule_setting_file = get_kmodule_setting_file(d)
    # kssesion_configs = detail_policy_parser(kmodule_setting_file)
    #
    # conn = conn_to_mysql()
    # cursor = conn.cursor()
    # rule_sql_template = u"insert into risk_engine_rule ({0}) VALUES ({1})"
    # policy_sql_template = u"insert into risk_engine_policy ({0}) VALUES ({1})"
    # rule_pkg_sql_template = u"insert into risk_engine_rule_rule_pkg (rule_id, policy_id) VALUES ({0}, {1})"
    #
    # for rule in rules:
    #     sql = rule_sql_template.format(*fill_k_v_sql(rule))
    #     cursor.execute(sql)
    # for rule_pkg in rule_rule_pkg:
    #     sql = rule_pkg_sql_template.format(rule_pkg[''])
    # for kssesion_config in kssesion_configs:
    #     sql = policy_sql_template.format(*fill_k_v_sql(kssesion_config))
    #     cursor.execute(sql)
    #
    # conn.commit()
    # conn.close()

# test()

