from django.contrib import admin
from users.models import Employees, Teams, Userlevels


admin.site.register(Employees)
admin.site.register(Teams)
admin.site.register(Userlevels)
