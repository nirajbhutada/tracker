# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from riskmanagement.forms.RiskManagementForm import RiskManagementForm
from riskmanagement.models import RiskManagement
from effortdata.views import predicate_lead, predicate_manager


@login_required
def index(request):
    leadflag = predicate_lead(request.user)
    managerflag = predicate_manager(request.user)
    riskObjList = RiskManagement.objects.all()
    context = RequestContext(request,
                             {'username': request.user,
                              'leadflag': leadflag,
                              'managerflag': managerflag,
                              'riskObjList': riskObjList})
    return render_to_response("riskmanagement/risk_management_index.html",
                              context_instance=context)


@login_required
def submit_form(request, risk_id=None):
    leadflag = predicate_lead(request.user)
    managerflag = predicate_manager(request.user)
    risk = None
    user = request.user
    if risk_id:
        try:
            risk = RiskManagement.objects.get(id=risk_id)
        except ObjectDoesNotExist:
            risk = None

    if request.method == 'POST':
        form = RiskManagementForm(risk, request.POST)
        print request.POST
        #if form.is_valid():
        #data = form.cleaned_data

        form.handle(request.POST, user, risk)
        return HttpResponseRedirect('/riskmanagement/')
    else:
        form = RiskManagementForm(risk)
    context = RequestContext(request, {'form': form,
                                       'leadflag': leadflag,
                                       'managerflag': managerflag,
                                       'username': user})
    return render_to_response("riskmanagement/riskinsertform.html",
                              context_instance=context)


@login_required
def delete_risk(request, risk_id):
    if risk_id:
        risk = RiskManagement.objects.get(id=risk_id)
        risk.delete()
    return HttpResponseRedirect('/riskmanagement/')
