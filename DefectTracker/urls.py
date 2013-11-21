from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.contrib.auth.views import password_change

urlpatterns = patterns('',
    # Examples:
     #url(r'^$', 'DefectTracker.views.home', name='home'),
     url(r'^admin/', include(admin.site.urls)),
     (r'pwreset/', password_change, {'post_change_redirect': '/login'}),
     (r'pwreset/', include('django.contrib.auth.urls')),
     url(r'team/$', 'users.teams.index', name="team_index"),
     url(r'team/add/$', 'users.teams.submit_form', name="team_add"),
     url(r'team/delete/$', 'users.teams.delete_team', name="team_delete"),
     url(r'login/$', 'users.dashboard.login', name="user_login"),
     url(r'logout/$', 'users.dashboard.logout', name="user_logout"),
     url(r'^riskmanagement/', include('riskmanagement.urls')),
     url(r'^release/', include('releasedata.urls')),
     url(r'^report/', include('effortdata.urls')),
     url(r'^profile/$', 'users.views.profile', name="profile"),
     url(r'^profile/(?P<emp_id>[0-9a-zA-Z_.]+)/$', 'users.views.profile', name="profile_edit"),
     url(r'^$', 'users.dashboard.index', name="index"),

)
import settings
urlpatterns += patterns("django.views",
                        url(r"%s(?P<path>.*)$" % settings.MEDIA_URL[1:],
                            "static.serve",
                            {"document_root": settings.MEDIA_ROOT}),
                            )
