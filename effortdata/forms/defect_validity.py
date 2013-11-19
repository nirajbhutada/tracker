'''
Created on 30-Jun-2012

@author: vijay
'''
from datetime import datetime

from django import forms
from django.contrib.auth.models import User
from users.models import Teams
from releasedata.models import Release, ReleasePhase
from effortdata.models import Defectvalidity, Target
from riskmanagement.forms import widgets


class DefectValidityForm(forms.Form):

    valid_date = forms.DateField(label='Date', required=False, input_formats=['%d-%m-%Y'])
    total_defects = forms.IntegerField(label='Total Defects')
    dup_defects = forms.IntegerField(label='Duplicate Defects')
    new_defects = forms.IntegerField(label='New Defects')
    fixed_defects = forms.IntegerField(label='Fixed Defects')
    cosmic_defects = forms.IntegerField(label='Cosmic Defects')
    obsol_defects = forms.IntegerField(label='Obsol Defects')

    def handle(self, data=False, user=None, defValidObj=None):
        teamobj = Teams.objects.get(id=data['team'])
        release = Release.objects.get(id=data['release'])
        release_phase = ReleasePhase.objects.get(id=data['releasephase'])
        valid_date = datetime.strptime(data['valid_date'], '%m-%d-%Y')
        if defValidObj:
            defValidObj.team = teamobj
            defValidObj.release = release
            defValidObj.release_phase = release_phase
            defValidObj.valid_date = valid_date
            defValidObj.total_defects = int(data['total_defects'])
            defValidObj.dup_defects = int(data['dup_defects'])
            defValidObj.new_defects = int(data['new_defects'])
            defValidObj.fixed_defects = int(data['fixed_defects'])
            defValidObj.cosmic_defects = int(data['cosmic_defects'])
            defValidObj.obsol_defects = int(data['obsol_defects'])

        else:
            defValidObj = Defectvalidity(team=teamobj,
                                    release=release,
                                    release_phase=release_phase,
                                    valid_date=valid_date,
                                    total_defects=int(data['total_defects']),
                                    dup_defects=int(data['dup_defects']),
                                    new_defects=int(data['new_defects']),
                                    fixed_defects=int(data['fixed_defects']),
                                    cosmic_defects=int(data['cosmic_defects']),
                                    obsol_defects=int(data['obsol_defects'])
                                    )
        defValidObj.save()

    def __init__(self, obj=False, user=None, *largs, **kargs):
        vals = dict()

        if obj:
            valid_date = (obj.valid_date).strftime('%m-%d-%Y')
            vals['valid_date'] = valid_date
            vals['release'] = obj.release.id
            vals['releasephase'] = obj.release_phase.id
            vals['total_defects'] = obj.total_defects
            vals['dup_defects'] = obj.dup_defects
            vals['new_defects'] = obj.new_defects
            vals['fixed_defects'] = obj.fixed_defects
            vals['cosmic_defects'] = obj.cosmic_defects
            vals['obsol_defects'] = obj.obsol_defects

        else:
            vals['total_defects'] = 0
            vals['dup_defects'] = 0
            vals['new_defects'] = 0
            vals['fixed_defects'] = 0
            vals['cosmic_defects'] = 0
            vals['obsol_defects'] = 0
            vals['valid_date'] = datetime.today().strftime('%m-%d-%Y')

        super(DefectValidityForm, self).__init__(initial=vals, *largs, **kargs)
#        if not obj:
        release = widgets.UnValidatedChoiceField(label="Release",
                                             choices=[[x.id, x.relname] for x in Release.objects.all()])
        releasephase = widgets.UnValidatedChoiceField(label="Release Phases",
                                             choices=[[x.id, x.release_phase] for x in ReleasePhase.objects.all()])
        team = widgets.UnValidatedChoiceField(label="Team",
                                          choices=[[x.id, x.teamname] for x in Teams.objects.all()])
        self.fields.insert(2, 'release', release)
        self.fields.insert(3, 'releasephase', releasephase)
        self.fields.insert(4, 'team', team)


class TargetForm(forms.Form):
    manualtcexectar = forms.FloatField(label="Manual TC", required=True,
            error_messages={'invalid': 'Manual TC should be Float',
                        'required': 'Manual TC  is not valid value'
            })
    autotcexectar = forms.FloatField(label="Auto TC", required=True,
         error_messages={
             'invalid': 'Auto TC should be Float',
             'required': 'Auto TC  is not valid value'
        })
    prsveritar = forms.FloatField(label="PR Verification", required=True,
        error_messages={
            'invalid': 'PR Verification should be Float',
             'required': 'PR Verification  is not valid value'
        })
    tcwritar = forms.FloatField(label="TC Written", required=True,
        error_messages={
            'invalid': 'TC Written should be Float',
            'required': 'TC Written is not valid value'
        })
    completionpercentage = forms.FloatField(label="Completed Percent",
                required=True,
        error_messages={
            'invalid': 'Completed Percent should be Float',
            'required': 'Completed Percent is not valid value'
        })

    def check_int(self, field_name):
        field_value = self.cleaned_data[field_name]
        try:
            field_value = int(self.cleaned_data[field_name])
            if  not(field_value >= 0):
                self._errors[field_name] =  \
                "%s should positive number" % self.fields[field_name].label
        except:
            self._errors[field_name] = \
            "%s should be positive number" % self.fields[field_name].label
        return field_value

    def check_float(self, field_name):
        try:
            field_value = self.cleaned_data[field_name]
        except Exception, e:
            print e
            field_value = ''
        try:
            field_value = float(self.cleaned_data[field_name])
            if  not(field_value >= 0.0):
                self._errors[field_name] = \
                "%s should be Positve Float number" \
                    % self.fields[field_name].label
        except:
            self._errors[field_name] = \
             "%s should  Positve Float number" % self.fields[field_name].label
        return field_value

    def clean_completionpercentage(self):
        self.check_float('manualtcexectar')
        self.check_float('autotcexectar')
        self.check_float('prsveritar')
        self.check_float('tcwritar')
        self.check_float('completionpercentage')

    def clean_team(self):
        data = self.cleaned_data['team']
        if int(data):
            return data
        else:
            raise forms.ValidationError('Team is Required')

    def clean_release(self):
        data = self.cleaned_data['release']
        if int(data):
            return data
        else:
            raise forms.ValidationError('Release is Required')

    def clean_releasephase(self):
        data = self.cleaned_data['releasephase']
        if int(data):
            return data
        else:
            raise forms.ValidationError('Release Phase is Required')

    def handle(self, data=False, user=None, target=None):
        teamobj = Teams.objects.get(id=data['team'])
        release = Release.objects.get(id=data['release'])
        releasephase = ReleasePhase.objects.get(id=data['releasephase'])
        if target:
            target.team = teamobj
            target.release = release
            target.release_phase = releasephase
            target.manualtcexectar = float(data['manualtcexectar'])
            target.autotcexectar = float(data['autotcexectar'])
            target.prsveritar = float(data['prsveritar'])
            target.tcwritar = float(data['tcwritar'])
            target.completionpercentage = float(data['completionpercentage'])
#            target.emp = user
            target.updated_by = user
            target.updated_datetime = datetime.now()
        else:
            target = Target(team=teamobj,
                            release=release,
                            release_phase=releasephase,
                            manualtcexectar=float(data['manualtcexectar']),
                            autotcexectar=float(data['autotcexectar']),
                            prsveritar=float(data['prsveritar']),
                            tcwritar=float(data['tcwritar']),
                            completionpercentage=float(data['completionpercentage']),
                            emp=user,
                            updated_by=user,
                            updated_datetime=datetime.now()
                            )
        target.save()

    def __init__(self, target=False, user=None, *largs, **kargs):
        vals = dict()
        if target:
            vals['manualtcexectar'] = float(target.manualtcexectar)
            vals['autotcexectar'] = target.autotcexectar
            vals['prsveritar'] = target.prsveritar
            vals['tcwritar'] = target.tcwritar
            vals['completionpercentage'] = target.completionpercentage
            vals['team'] = target.team.id
            vals['release'] = target.release.id
            vals['releasephase'] = target.release_phase.id

        else:
            vals['manualtcexectar'] = 0.0
            vals['autotcexectar'] = 0.0
            vals['prsveritar'] = 0.0
            vals['tcwritar'] = 0.0
            vals['completionpercentage'] = 0.0
        super(TargetForm, self).__init__(initial=vals, *largs, **kargs)
        choices = [[0, 'Select One']]
        choices.extend([(x.id, x.relname) for x in Release.objects.all()])
        release = widgets.UnValidatedChoiceField(label="Release",
                                             choices=choices, required=True,
                                             error_messages={'required':'Release is Required'})

        choices = [[0, 'Select One']]
        choices.extend([(x.id, x.release_phase) for x in ReleasePhase.objects.all()])
        releasephase = widgets.UnValidatedChoiceField(label="Release Phases",
                                             choices=choices, required=True,
                                             error_messages={'required':'Release Phases is Required'})

        choices = [[0, 'Select One']]
        choices.extend([(t.id, t.teamname) for t in Teams.objects.all()])
        team = widgets.UnValidatedChoiceField(label="Team",
                                              choices=choices, required=True,
                                              error_messages={'required':'Team is Required'})
        self.fields.insert(2, 'release', release)
        self.fields.insert(3, 'releasephase', releasephase)
        self.fields.insert(4, 'team', team)
