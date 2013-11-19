'''
Created on 23-Jun-2012

@author: vijay
'''
import urllib
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist

from users.forms import TeamForm
from users.models import Teams
from effortdata.views import predicate_lead, predicate_manager


@login_required
def index(request):
    '''presently index page just render static page and returns it back'''
    leadflag = predicate_lead(request.user)
    managerflag = predicate_manager(request.user)
    teams = Teams.objects.all().order_by('-id')
    if request.GET.get('name', False):
        teams = teams.filter(teamname__icontains=request.GET['name'])
    offset = int(request.GET.get("offset", 0))
    nsubs = teams.count()
    teams = teams[offset:offset + 10]
    pages = [urllib.urlencode(dict(name=request.GET.get('name', ''),
                                   offset=i)) for i in range(0, nsubs, 10)]
    template = loader.get_template('users/team/team_index.html')

    context = RequestContext(request,
                             {'username': request.user,
                              'leadflag': leadflag,
                              'managerflag': managerflag,
                              'teams': teams,
                              'pages': pages,
                              'offset': (offset + 10) / 10,
                              'curr_name': request.GET.get('name', '')})
    return HttpResponse(template.render(context))


@login_required
def submit_form(request):
    leadflag = predicate_lead(request.user)
    managerflag = predicate_manager(request.user)
    teamObj = None
    user = request.user
    team_id = request.GET.get('team_id', None)
    if team_id:
        try:
            teamObj = Teams.objects.get(id=team_id)
        except ObjectDoesNotExist:
            pass
    if request.method == 'POST':
        form = TeamForm(teamObj, request.POST)

        if form.is_valid():
            data = form.cleaned_data
            form.handle(data, teamObj)
            context = RequestContext(request, {})
            return HttpResponseRedirect('/team/')

    else:
        form = TeamForm(teamObj)
    context = RequestContext(request, {'form': form,
                                       'leadflag': leadflag,
                                       'managerflag': managerflag,
                                       'username': user})
    return render_to_response("users/team/teaminsert.html",
                              context_instance=context)


@login_required
def delete_team(request):
    team_id = request.GET.get('team_id', None)
    if team_id:
        team = Teams.objects.get(id=team_id)
        team.delete()
    return HttpResponseRedirect('/team/')
