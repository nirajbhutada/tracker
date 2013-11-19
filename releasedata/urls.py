'''
Created on 22-Jun-2012

@author: vijay
'''
from django.conf.urls.defaults import *

urlpatterns = patterns ('',

                url(r'phase/$', 'releasedata.views.phase_index', name='phase'),
                url(r'phase/add/$', 'releasedata.views.release_phase_form', name='phase_form'),
                url(r'phase/edit/(?P<phase_id>[0-9.]+)/$', 'releasedata.views.release_phase_form', name='phase_edit'),
                url(r'phase/delete/(?P<phase_id>[0-9.]+)/$', 'releasedata.views.delete_release_phase', name='phase_delete'),
                url(r'^$', 'releasedata.views.index', name='release'),
                url(r'add/$', 'releasedata.views.release_form', name='release_form'),
                url(r'edit/(?P<release_id>[0-9.]+)/$', 'releasedata.views.release_form', name='release_edit'),
                url(r'delete/(?P<release_id>[0-9.]+)/$', 'releasedata.views.delete_release', name='release_delete'),
    )
