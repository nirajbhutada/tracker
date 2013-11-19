'''
Created on 22-Jun-2012

@author: vijay
'''
from django.conf.urls.defaults import *

urlpatterns = patterns ('',
                url(r'^$', 'riskmanagement.views.index'),
                url(r'add/$', 'riskmanagement.views.submit_form'),
                url(r'add/(?P<risk_id>[0-9.]+)/$', 'riskmanagement.views.submit_form'),
                url(r'delete/(?P<risk_id>[0-9.]+)/$', 'riskmanagement.views.delete_risk'),
    )
