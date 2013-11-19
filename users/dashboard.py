'''
Created on 20-Jun-2012

@author: vijay
'''
import datetime
from django.contrib.auth.models import User
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from effortdata.views import predicate_lead, predicate_manager
from effortdata.models import Effortdata,Target

@login_required
def index(request):
    '''presently index page just render static page and returns it back'''
    leadflag = predicate_lead(request.user)
    managerflag = predicate_manager(request.user)
    target_list = Target.objects.filter(emp=request.user)
#    target_dict = {}
#    for target in target_list:
#        target_dict.default(target.release.relname, {})
#        target_dict[target.release.relname]\
#            .default(target.release_phase.release_phase, [])

    return render_to_response("index.html",
                        {'username': request.user,
                        'target_list':target_list,
                        'leadflag': leadflag,
                        'managerflag': managerflag, })


def login(request):

    if request.method == "POST":
        form = AuthenticationForm(None, request.POST)
        redirect_url = request.REQUEST.get('next', '')
        if form.is_valid():
            django_login(request, form.user_cache)
            request.session['username'] = form.user_cache
            user = User.objects.get(id=form.get_user_id)
            user.last_login = datetime.datetime.now()
            user.save()
            if not redirect_url:
                redirect_url = '/'
            return HttpResponseRedirect(redirect_url)

    else:
        form = AuthenticationForm()

    context = RequestContext(request, dict(form=form,
                                           next=request.GET.get('next', '')))
    print context
    return render_to_response("users/login.html", context_instance=context)


def logout(request):
    request.session.clear()
    django_logout(request)
    request.session['message'] = "You are now logged out. See you soon!"
    return HttpResponseRedirect(reverse('user_login'))


def change_password(request):
    user = request.user
    template = loader.get_template('users/change_password.html')
    if request.method == 'POST':
        form = ChangePwdForm(request.POST)
        if form.is_valid():
            if not user.check_password(form.data['old_password']):
                form.errors['__all__'] = 'Incorrect Old Password'
            else:
                user.set_password(form.data['new_password'])
                user.save()
                return HttpResponseRedirect('/')
    else:
        form = ChangePwdForm()
    context = RequestContext(request, dict(form=form))
    return HttpResponse(template.render(context))
