# Create your views here.

from datetime import datetime
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from effortdata.views import predicate_lead, predicate_manager

from users.forms import EmployeeForm
from users.models import Employees

@login_required
def profile(request):
    leadflag = predicate_lead(request.user)
    managerflag = predicate_manager(request.user)
    employee = None
    user = request.user
    try:
        employee = Employees.objects.get(user=request.user)
        if employee.birthdate:
            birthdate = employee.birthdate.strftime('%Y-%m-%d')
        else:
            birthdate = datetime.now().strftime('%Y-%m-%d')
        if employee.hiredate:
            hiredate = employee.hiredate.strftime('%Y-%m-%d')
        else:
            hiredate = datetime.now().strftime('%Y-%m-%d')
    except ObjectDoesNotExist:
        birthdate = datetime.now().strftime('%Y-%m-%d')
        hiredate = datetime.now().strftime('%Y-%m-%d')

    if request.method == 'POST':
        form = EmployeeForm(employee, request.POST)
        data = request.POST
        flag = form.handle(data, request.user, employee)
        if flag:
            return HttpResponseRedirect('/')

    else:
        form = EmployeeForm(employee)
    print form
    context = RequestContext(request, {'form': form,
                                       'leadflag': leadflag,
                                       'managerflag': managerflag,
                                       'username': user,
                                       'birthdate':birthdate,
                                       'hiredate':hiredate
                                       })
    return render_to_response("users/profile.html",
                              context_instance=context)
