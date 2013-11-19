# Create your views here.

import urllib
from datetime import datetime
from datetime import date
from datetime import timedelta

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator

import xlwt

from effortdata.forms.effort_form import EffortForm
from effortdata.forms.defect_validity import DefectValidityForm, TargetForm
from effortdata.models import Effortdata, Defectvalidity, Target
from users.models import Teams
from releasedata.models import Release, ReleasePhase


def predicate_lead(u):
    """Authentication predicate used for the controller methods in the """

    if u.is_authenticated() and u.groups.filter(name="leads"):
            return True
    return False


def predicate_manager(u):
    """Authentication predicate used for the controller methods in the
    """
    if u.is_authenticated() and u.groups.filter(name="managers"):
            return True
    return False


@login_required
def index(request):
    leadflag = predicate_lead(request.user)
    managerflag = predicate_manager(request.user)
    message = ''
    if managerflag:
        effortlist = Effortdata.objects.all().order_by('release__relname')
    elif leadflag:
        try:
            teamobj_list = Teams.objects.filter(lead__id=request.user.id)
            effortlist = Effortdata.objects.filter(team__in=teamobj_list)\
                            .order_by('release__relname')
        except:
            effortlist = Effortdata.objects.filter(emp=request.user)\
                        .order_by('release__relname')
    else:
        effortlist = Effortdata.objects.filter(emp=request.user)\
                    .order_by('release__relname')

    curr_team_id = request.GET.get('team', 'all')
    curr_release_name = request.GET.get('release', 'all')
    curr_phase_name = request.GET.get('phase', 'all')
    curr_user_id = request.GET.get('user', 'all')
    end_date = request.GET.get('date_input_end', None)
    start_date = request.GET.get('date_input_start', None)
    if end_date and not start_date:
        start_date = (end_date + timedelta(-7))
    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')
    if not start_date:
        start_date = (datetime.now() + timedelta(-7)).strftime('%Y-%m-%d')

    if curr_team_id and curr_team_id != 'all':
        effortlist = effortlist.filter(team__id=curr_team_id)
    if curr_release_name and curr_release_name != 'all':
        effortlist = effortlist.filter(release__id=curr_release_name)
    if curr_phase_name and curr_phase_name != 'all':
        effortlist = effortlist.filter(release_phase__id=curr_phase_name)
    if curr_user_id and curr_user_id != 'all':
        effortlist = effortlist.filter(emp__id=curr_user_id)
    users_list = [(str(t.id), '%s %s' % (t.first_name, t.last_name))
                  for t in User.objects.select_related('id', 'username')
                           if t.username != 'admin']
    users_list.insert(0, ('all', 'all'))
    if end_date and managerflag:
        effortlist = effortlist.filter(
                            effort_date__range=[start_date, end_date])

    teams_list = [(str(t.id), t.teamname)
                  for t in Teams.objects.select_related('id', 'teamname')]
    teams_list.insert(0, ('all', 'all'))

    releaselist = [(str(r.id), r.relname)
                   for r in Release.objects.select_related('id', 'relname')\
                   .filter(active=True)]
    releaselist.insert(0, ('all', 'all'))
    phaselist = [(str(p.id), p.release_phase)
                 for p in ReleasePhase.objects\
                     .select_related('id', 'release_phase').filter(active=True)]
    phaselist.insert(0, ('all', 'all'))

    p = Paginator(effortlist, 15)
    offset = int(request.GET.get("offset", 0))
    nsubs = effortlist.count()
    effortlist = effortlist

    pages = [urllib.urlencode(dict(release=curr_release_name,
                                   team=curr_team_id,
                                   phase=curr_phase_name,
                                   user=curr_user_id,
                                   date_input_start=start_date,
                                   date_input_end=end_date,
                                   offset=i)) for i in range(0, nsubs, 15)]
    context = RequestContext(request,
                             {'username': request.user,
                              'effortlist': effortlist,
                              'message': message,
                              'leadflag': leadflag,
                              'managerflag': managerflag,
                              'is_manager': managerflag,
                              'teams_list': teams_list,
                              'release_names_list': releaselist,
                              'phase_names_list': phaselist,
                              'pages': pages,
                              'p': p,
                              'users_list': users_list,
                              'curr_user_id':  '%s' % curr_user_id,
                              'curr_team_id': '%s' % curr_team_id,
                              'curr_release_id': '%s' % curr_release_name,
                              'curr_phase_id': '%s' % curr_phase_name,
                              'curr_start_date': start_date,
                              'curr_end_date': end_date,
                              'offset': (offset + 15) / 15,
                              'prev_url': request.META['QUERY_STRING']})

    return render_to_response("effortdata/effort_index.html",
                              context_instance=context)


def export_excel(request):

#    start_date, end_date = request.session['efforts_data']
    headers = ['Release', 'Teams', 'Planned For The week',
               'Actual Completed For The week', '% Schedule Variance',
               'Target For Release', 'Actual till date',
               '% Complete till date']

    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('reports')

    heading_style = xlwt.easyxf('font: bold on, italic on; pattern: pattern solid, fore-colour grey25; align: wrap on, horiz center;')

    row = 0
    default_style = xlwt.Style.default_style
    start = datetime.strptime('2012-07-18', '%Y-%m-%d')
    date_ranges = [start + timedelta(days=x) for x in range(0, 10000, 7) if start + timedelta(days=x) <= datetime.now()]

    curr_team_id = request.GET.get('team', 'all')
    curr_release_name = request.GET.get('release', 'all')
    curr_phase_name = request.GET.get('phase', 'all')
    end_date = request.GET.get('date_input_end', None)
    start_date = request.GET.get('date_input_start', None)

    if curr_team_id and curr_team_id != 'all':
        team_obj = Teams.objects.get(id=curr_team_id)
        team_list = [team_obj]
    else:
        team_list = Teams.objects.all()
    if curr_release_name and curr_release_name != 'all':
        release_obj = Release.objects.get(id=curr_release_name)
        releaselist = [release_obj]
    else:
        releaselist = Release.objects.filter(active=True)

    if curr_phase_name and curr_phase_name != 'all':
        release_phase_obj = ReleasePhase.objects.get(id=curr_phase_name)
        release_phase_list = [release_phase_obj]
    else:
        release_phase_list = [phase for phase in
                                ReleasePhase.objects.filter(active=True)]

    try:
        for release in releaselist:
            for idx, i in enumerate(headers):
                sheet.write(row, idx, i, heading_style)
                sheet.col(idx).width = 5000
            release_flag = True
            for team in team_list:
                row = row + 1
                if release_flag:
                    sheet.write(row, 0, release.relname, style=default_style)
                    release_flag = False
                sheet.write(row, 1, team.teamname, style=default_style)
                effortlist = Effortdata.objects.filter(team=team)\
                        .filter(release=release)\
                        .filter(effort_date__range=[start_date, end_date])\
                        .filter(release_phase__in=release_phase_list)

                if curr_phase_name and curr_phase_name != 'all':
                    effortlist = effortlist\
                                .filter(release_phase__id=curr_phase_name)

                plannedno = 0
                executedno = 0
                variance = 0.0
                for effort in effortlist:
                    plannedno += effort.testcasesplannedno
                    executedno += effort.testcasesexecutedno
                try:
                    variance = ((executedno - plannedno) / plannedno) * 100
                except:
                    pass

                sheet.write(row, 2, plannedno, style=default_style)
                sheet.write(row, 3, executedno, style=default_style)
                sheet.write(row, 4, variance, style=default_style)
                # apply targets
                till_date_list = []
                for idx in range(0, len(date_ranges) + 1):
                    if idx + 1 < len(date_ranges):
                        effortlist = Effortdata.objects.filter(team=team)\
                                    .filter(release=release)\
                                    .filter(release_phase__in = release_phase_list)\
                                .filter(effort_date__range=[date_ranges[idx].strftime('%Y-%m-%d'), date_ranges[idx + 1].strftime('%Y-%m-%d')])
                        till_date_testcasesexecuted = sum([effort.testcasesexecutedno  for effort in effortlist])
                        till_date_list.append(till_date_testcasesexecuted)

                target_list = Target.objects.filter(team=team)\
                    .filter(release=release)\
                    .filter(release_phase__in=release_phase_list)

                total = 0
                for t in target_list:
                    total += sum([t.manualtcexectar, t.autotcexectar,
                                                t.prsveritar])
                sheet.write(row, 5, total, style=default_style)
                till_date_sum = sum(till_date_list)
                try:
                    percent = ((total - (total - till_date_sum)) / total) * 100
                except:
                    percent = 0.00
                sheet.write(row, 6, '%s' % (sum(till_date_list)), style=default_style)
                sheet.write(row, 7, '% 0.2f' % (percent), style=default_style)
            row = row + 2
    except Exception, e:
        print e

    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = \
            'attachment; filename=efforts_%s_to_%s.xls' % (start_date, end_date)
    book.save(response)
    return response


@login_required
def submit_form(request, effort_id=None):
    leadflag = predicate_lead(request.user)
    managerflag = predicate_manager(request.user)
    effort = None
    user = request.user
    if effort_id:
        try:
            effort = Effortdata.objects.get(id=effort_id)
        except ObjectDoesNotExist:
            effort = None

    if request.method == 'POST':
        form = EffortForm(effort=effort, user=user, data=request.POST)
        data = request.POST
        if form.is_valid():
            form.handle(data, user, effort)
            return HttpResponseRedirect('/report/')

    else:

        form = EffortForm(effort=effort, user=user)
    context = RequestContext(request, {'form': form,
                                       'leadflag': leadflag,
                                       'managerflag': managerflag,
                                       'username': user})
    return render_to_response("effortdata/effortinsertform.html",
                              context_instance=context)


@login_required
def delete_effort(request, effort_id):
    if effort_id:
        effort = Effortdata.objects.get(id=effort_id)
        effort.delete()
    return HttpResponseRedirect('/report/')


@login_required
def defect_index(request):
    leadflag = predicate_lead(request.user)
    managerflag = predicate_manager(request.user)
    defvalObj = Defectvalidity.objects.all()
    context = RequestContext(request,
                             {'username': request.user,
                              'leadflag': leadflag,
                              'managerflag': managerflag,
                              'defvalObj': defvalObj})

    return render_to_response("effortdata/defect_validity/def_validity_index.html",
                              context_instance=context)


@login_required
def defect_validity_submit_form(request, defvalidity_id=None):
    leadflag = predicate_lead(request.user)
    managerflag = predicate_manager(request.user)
    defect = None
    user = request.user
    if defvalidity_id:
        try:
            defect = Defectvalidity.objects.get(id=defvalidity_id)
        except ObjectDoesNotExist:
            defect = None

    if request.method == 'POST':
        form = DefectValidityForm(obj=defect, user=user, data=request.POST)
        data = request.POST
        if form.is_valid():
            form.handle(data, user, defect)
            return HttpResponseRedirect('/report/defect_validity/')

    else:
        form = DefectValidityForm(obj=defect, user=user)
    context = RequestContext(request, {'form': form,
                                       'leadflag': leadflag,
                                       'managerflag': managerflag,
                                       'username': user})
    return render_to_response("effortdata/defect_validity/def_validity_form.html",
                              context_instance=context)


@login_required
def delete_defect_validity(request, defvalidity_id):
    if defvalidity_id:
        defect_val = Defectvalidity.objects.get(id=defvalidity_id)
        defect_val.delete()
    return HttpResponseRedirect('/report/defect_validity/')


@login_required
def target_index(request):
    leadflag = predicate_lead(request.user)
    managerflag = predicate_manager(request.user)
    message = None
    if managerflag:
        targetlist = Target.objects.all()
    elif leadflag:
        try:
            teamobj_list = Teams.objects.filter(lead__id=request.user.id)
            targetlist = Target.objects.filter(team__in=teamobj_list)
        except:
            message = "No team assign for lead %s" % (request.user.first_name)
    else:
        targetlist = Target.objects.filter(emp=request.user)

    curr_team_id = request.GET.get('team', 'all')
    curr_release_name = request.GET.get('release', 'all')
    curr_user_id = request.GET.get('user', 'all')

    if curr_team_id and curr_team_id != 'all':
        targetlist = targetlist.filter(team__id=curr_team_id)
    if curr_release_name and curr_release_name != 'all':
        targetlist = targetlist.filter(release__id=curr_release_name)
    if curr_user_id and curr_user_id != 'all':
        targetlist = targetlist.filter(emp__id=curr_user_id)

    teams_list = [(str(t.id), t.teamname)
                  for t in Teams.objects.select_related('id', 'teamname')]
    teams_list.insert(0, ('all', 'all'))
    releaselist = [(str(r.id), r.relname)
                   for r in Release.objects.select_related('id', 'relname')\
                   .filter(active=True)]
    releaselist.insert(0, ('all', 'all'))
    users_list = [(str(t.id), '%s %s' % (t.first_name, t.last_name))
                  for t in User.objects.select_related('id', 'username') if t.username != 'admin']
    users_list.insert(0, ('all', 'all'))

    p = Paginator(targetlist, 15)
    offset = int(request.GET.get("offset", 0))
    nsubs = targetlist.count()
    targetlist = targetlist

    pages = [urllib.urlencode(dict(release=curr_release_name,
                                   team=curr_team_id,
                                   offset=i)) for i in range(0, nsubs, 15)]

    context = RequestContext(request,
                             {'username': request.user,
                              'leadflag': leadflag,
                              'managerflag': managerflag,
                              'message': message,
                              'teams_list': teams_list,
                              'users_list': users_list,
                              'release_names_list': releaselist,
                              'curr_team_id': '%s' % curr_team_id,
                              'curr_release_id': '%s' % curr_release_name,
                              'curr_user_id': '%s' % curr_user_id,
                              'pages': pages,
                              'p': p,
                              'offset': (offset + 15) / 15,
                              'targetlist': targetlist})
    return render_to_response("effortdata/target/target_index.html",
                              context_instance=context)


def target_export_excel(request):
    headers = ['Employee Name', 'Release', 'Teams', 'Manual TC Execution target',
               'Auto TC Execution Target', "PR's Verified target",
               'Test Case Writing Target', 'Completion %']

    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('targets')

    heading_style = xlwt.easyxf('font: bold on, italic on; pattern: pattern solid, fore-colour grey25; align: wrap on, horiz center;')

    row = 0
    default_style = xlwt.Style.default_style

    curr_team_id = request.GET.get('team', 'all')
    curr_release_name = request.GET.get('release', 'all')
    curr_user_id = request.GET.get('user', 'all')

    if curr_team_id and curr_team_id != 'all':
        team_obj = Teams.objects.get(id=curr_team_id)
        team_list = [team_obj]
    else:
        team_list = Teams.objects.all()
    if curr_release_name and curr_release_name != 'all':
        release_obj = Release.objects.get(id=curr_release_name)
        releaselist = [release_obj]
    else:
        releaselist = Release.objects.all()
    if curr_user_id and curr_user_id != 'all':
        user_obj = Release.objects.get(id=curr_release_name)
        userslist = [user_obj]
    else:
        userslist = [u for u in User.objects.all() if u.username != 'admin']

    try:
                    for idx, i in enumerate(headers):
                        sheet.write(row, idx, i, heading_style)
                        sheet.col(idx).width = 5000
#        for user in userslist:
#            for idx, i in enumerate(headers):
#                sheet.write(row, idx, i, heading_style)
#                sheet.col(idx).width = 5000
#            user_flag = True
#
#            for release in releaselist:
#                row = row + 1
#                if user_flag:
#                    sheet.write(row, 0, user.username, style=default_style)
#                    user_flag = False
#                release_flag = True
                #for team in team_list:
#                    if release_flag:
#                        sheet.write(row, 1, release.relname, style=default_style)
#                        release_flag = False
                    #sheet.write(row, 2, team.teamname, style=default_style)

                    targetlist = Target.objects.filter(team__in=team_list).filter(release__in=releaselist).filter(emp__in=userslist)
                    for target in targetlist:
                        row = row + 1
                        #manualtcexectar = 0.0
                        #autotcexectar = 0.0
                        #prsveritar = 0.0
                        #tcwritar = 0.0
                        #completionpercentage = 0.0

                        #manualtcexectar = sum([target.manualtcexectar  for target in targetlist])
                        #autotcexectar = sum([target.autotcexectar  for target in targetlist])
                        #prsveritar = sum([target.prsveritar  for target in targetlist])
                        #tcwritar = sum([target.tcwritar   for target in targetlist])
                        #completionpercentage = sum([target.completionpercentage   for target in targetlist])

                        #if targetlist:
                        #    completionpercentage = completionpercentage / len(targetlist)
                        sheet.write(row, 0, '%s %s' % (target.emp.first_name, target.emp.last_name), style=default_style)
                        sheet.write(row, 1, target.release.relname, style=default_style)
                        sheet.write(row, 2, target.team.teamname, style=default_style)
                        sheet.write(row, 3, target.manualtcexectar, style=default_style)
                        sheet.write(row, 4, target.autotcexectar, style=default_style)
                        sheet.write(row, 5, target.prsveritar, style=default_style)
                        sheet.write(row, 6, target.tcwritar, style=default_style)
                        sheet.write(row, 7, target.completionpercentage, style=default_style)



    except Exception, e:
        print e

    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=targets_%s.xls' % (datetime.now())
    book.save(response)
    return response


@login_required
def target_submit_form(request, target_id=None):
    leadflag = predicate_lead(request.user)
    managerflag = predicate_manager(request.user)
    target = None
    user = request.user
    if target_id:
        try:
            target = Target.objects.get(id=target_id)
        except ObjectDoesNotExist:
            target = None

    if request.method == 'POST':
        form = TargetForm(target=target, user=user, data=request.POST)
        data = request.POST
        if form.is_valid():
            form.handle(data, user, target)
            return HttpResponseRedirect('/report/target/')

    else:
        form = TargetForm(target=target, user=user)

    context = RequestContext(request, {'form': form,
                                       'leadflag': leadflag,
                                       'managerflag': managerflag,
                                       'username': user})
    return render_to_response("effortdata/target/target_form.html",
                              context_instance=context)


@login_required
def delete_target(request, target_id):
    if target_id:
        target = Target.objects.get(id=target_id)
        target.delete()
    return HttpResponseRedirect('/report/target/')
