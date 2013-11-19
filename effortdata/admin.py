'''
Created on 28-Jun-2012

@author: vijay
'''
from django.contrib import admin
from effortdata.models import Effortdata, Defectvalidity, IssueLog, Target, TaskType


admin.site.register(Effortdata)
admin.site.register(Defectvalidity)
admin.site.register(IssueLog)
admin.site.register(Target)
admin.site.register(TaskType)


#class EffortdataAdmin(admin.ModelAdmin):
#    pass
#
#admin.site.register(Effortdata, EffortdataAdmin)
