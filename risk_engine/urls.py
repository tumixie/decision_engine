from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^raw_data/row_keys$', views.row_keys, name='row_keys'),
    url(r'^raw_data/(?P<apply_no>.+)/row_keys', views.row_keys_detail, name='row_keys_detail'),
    url(r'^raw_data_detail/(?P<row_key>.+)$', views.raw_data_detail, name='raw_data_detail'),
    url(r'^work_flow/$', views.work_flow, name='work_flow'),
    url(r'^work_flow/process_id/(?P<process_id>[a-z0-9\-]+)', views.work_flow_detail_by_process_id,
        name='work_flow_detail_by_process_id'),
    url(r'^work_flow/apply_no/(?P<apply_no>[a-zA-Z0-9\-]+)', views.work_flow_detail_by_apply_no,
        name='work_flow_detail_by_apply_no'),
    url(r'^brms/?$', views.brms, name='brms'),
    url(r'^brms/util/?$', views.brms_util, name='brms_util'),
    url(r'^brms_detail/rules/$', views.BrmsDetailRule.as_view(), name='brms_detail_rule'),
    url(r'^brms_detail/rule_goups/', views.BrmsDetailRuleGroup.as_view(), name='brms_detail_rule_group'),
    url(r'^brms_detail/rules/id=(?P<id>[\d]+)', views.brms_detail_rule_by_id, name='brms_detail_rule_by_id'),
    url(r'brms_detail/rulegroup/id=(?P<id>[\d]+)', views.brms_detail_rule_group_by_id, name='brms_detail_rule_group_by_id'),
]
