'''
Created on 21-Jun-2012

@author: vijay
'''
from django import forms

from releasedata.models import Release, ReleasePhase


class ReleaseForm(forms.Form):
    relname = forms.CharField(max_length=90, label='Release Name',
                              required=True)

    def handle(self, data, release=None):
        "Handle submission of releases form"
        if not release:
            obj, created = Release.objects.get_or_create(relname=data['relname'])
            obj.save()
        else:
            release.relname = data['relname']
            release.save()

    def __init__(self, release=False, *largs, **kargs):
        vals = dict()

        if release:
            vals["relname"] = release.relname

        super(ReleaseForm, self).__init__(initial=vals, *largs, **kargs)


class ReleasePhaseForm(forms.Form):
    release_phase = forms.CharField(max_length=90, label='Release Phase Name',
                        required=True)

    def handle(self, data, phase=None):
        "Handle submission of releases form"
        if not phase:
            obj, created = ReleasePhase.objects.get_or_create(release_phase=data['release_phase'])
            obj.save()
        else:
            phase.release_phase = data['release_phase']
            phase.save()

    def __init__(self, phase=False, *largs, **kargs):
        vals = dict()

        if phase:
            vals["release_phase"] = phase.release_phase

        super(ReleasePhaseForm, self).__init__(initial=vals, *largs, **kargs)
