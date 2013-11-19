# Create your views here.
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from releasedata.forms.ReleaseForm import ReleaseForm, ReleasePhaseForm
from releasedata.models import Release, ReleasePhase
from effortdata.views import predicate_lead, predicate_manager


@login_required
def index(request):
    leadflag = predicate_lead(request.user)
    managerflag = predicate_manager(request.user)
    releaseslist = Release.objects.all()
    context = RequestContext(request,
                             {'username': request.user,
                              'leadflag': leadflag,
                              'managerflag': managerflag,
                              'releases': releaseslist})

    return render_to_response("releasedata/release_index.html",
                              context_instance=context)


@login_required
def release_form(request, release_id=None):
    leadflag = predicate_lead(request.user)
    managerflag = predicate_manager(request.user)
    release = None
    error_msg = None
    user = request.user
    if release_id:
        try:
            release = Release.objects.get(id=release_id)
        except ObjectDoesNotExist:
            release = None

    if request.method == 'POST':

        form = ReleaseForm(release, request.POST)
        if form.is_valid():
            data = form.cleaned_data
            form = form.handle(data, release)
            return HttpResponseRedirect('/release/')
        else:
            error_msg = 'Release Name is required'
            context = RequestContext(request, {'form': form,
                                       'leadflag': leadflag,
                                       'managerflag': managerflag,
                                       'error_msg':error_msg,
                                       'username': user})
            return render_to_response("releasedata/releaseinsertform.html",
                              context_instance=context)

    else:
        form = ReleaseForm(release)
    context = RequestContext(request, {'form': form,
                                       'leadflag': leadflag,
                                       'managerflag': managerflag,
                                       'username': user})
    return render_to_response("releasedata/releaseinsertform.html",
                              context_instance=context)


@login_required
def delete_release(request, release_id):
    if release_id:
        rel = Release.objects.get(id=release_id)
        rel.delete()
    return HttpResponseRedirect('/release/')


@login_required
def phase_index(request):
    leadflag = predicate_lead(request.user)
    managerflag = predicate_manager(request.user)
    releaseslist = ReleasePhase.objects.all()
    context = RequestContext(request,
                             {'username': request.user,
                              'leadflag': leadflag,
                              'managerflag': managerflag,

                              'releases': releaseslist})

    return render_to_response("releasedata/phase/phase_index.html",
                              context_instance=context)



@login_required
def release_phase_form(request, phase_id=None):
    leadflag = predicate_lead(request.user)
    managerflag = predicate_manager(request.user)
    phase = None
    user = request.user
    if phase_id:
        try:
            phase = ReleasePhase.objects.get(id=phase_id)
        except ObjectDoesNotExist:
            pass
    if request.method == 'POST':
        form = ReleasePhaseForm(phase, request.POST)

        if form.is_valid():
            data = form.cleaned_data
            f = form.handle(data, phase)
            return HttpResponseRedirect('/release/phase/')
        else:
            error_msg = 'Release Phase Name is required'
            context = RequestContext(request, {'form': form,
                                       'leadflag': leadflag,
                                       'managerflag': managerflag,
                                       'error_msg':error_msg,
                                       'username': user})
            return render_to_response("releasedata/phase/releasephaseinsertform.html",
                              context_instance=context)

    else:
        form = ReleasePhaseForm(phase)
    context = RequestContext(request, {'form': form,
                                       'leadflag': leadflag,
                                       'managerflag': managerflag,
                                       'username': user})
    return render_to_response("releasedata/phase/releasephaseinsertform.html",
                              context_instance=context)


@login_required
def delete_release_phase(request, phase_id):
    if phase_id:
        rel_phase = ReleasePhase.objects.get(id=phase_id)
        rel_phase.delete()
    return HttpResponseRedirect('/release/phase/')
