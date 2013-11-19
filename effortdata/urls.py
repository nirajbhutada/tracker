'''
Created on 22-Jun-2012

@author: vijay
'''
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'defect_validity/add/', 'effortdata.views.defect_validity_submit_form'),
    url(r'defect_validity/edit/(?P<defvalidity_id>[0-9.]+)/$', 'effortdata.views.defect_validity_submit_form'),
    url(r'defect_validity/delete/(?P<defvalidity_id>[0-9.]+)/$', 'effortdata.views.delete_defect_validity'),
    url(r'defect_validity/$', 'effortdata.views.defect_index'),
    url(r'target/add/', 'effortdata.views.target_submit_form'),
    url(r'target/edit/(?P<target_id>[0-9.]+)/$', 'effortdata.views.target_submit_form'),
    url(r'target/delete/(?P<target_id>[0-9.]+)/$', 'effortdata.views.delete_target'),
    url(r'target/$', 'effortdata.views.target_index'),
    url(r'add/$', 'effortdata.views.submit_form'),
    url(r'add/(?P<effort_id>[0-9a-zA-Z_.]+)/$', 'effortdata.views.submit_form'),
    url(r'delete/(?P<effort_id>[0-9a-zA-Z_.]+)/$', 'effortdata.views.delete_effort'),
    url(r'^$', 'effortdata.views.index'),
    url(r'target/export/$', 'effortdata.views.target_export_excel'),
    url(r'export/$', 'effortdata.views.export_excel'),
    )
