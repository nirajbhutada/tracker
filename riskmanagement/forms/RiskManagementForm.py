'''
Created on 22-Jun-2012

@author: vijay
'''
from datetime import datetime

from django import forms

from users.models import Teams
from riskmanagement.forms import widgets
from riskmanagement.models import RiskManagement


class RiskManagementForm(forms.Form):
    identificationdate = forms.DateField(label='Identification Date', required=False)
    riskdetail = forms.CharField(max_length=90, label='Risk Details', required=True)
    category = forms.CharField(max_length=90, label='Category', required=True)
    impact = forms.CharField(max_length=90, label='Impact', required=False)
    mitigationplan = forms.CharField(widget=forms.Textarea)
    contigencyplan = forms.CharField(widget=forms.Textarea)
    team = widgets.UnValidatedChoiceField(label="Team",
                     choices=[[x.id, x.teamname] for x in Teams.objects.all()])

    def handle(self, data, user, risk=None):
        "Handle submission of releases form"
        if risk:
            print data['identificationdate']
            team = Teams.objects.get(id=data['team'])
            risk.identificationdate = data['identificationdate']
            risk.riskdetail = data['riskdetail']
            risk.impact = data['impact']
            risk.category = data['category']
            risk.mitigationplan = data['mitigationplan']
            risk.contigencyplan = data['contigencyplan']
            risk.team = team
        else:
            team = Teams.objects.get(id=data['team'])
            risk = RiskManagement(identificationdate=data['identificationdate'],
                                  riskdetail=data['riskdetail'],
                                  impact=data['impact'],
                                  category=data['category'],
                                  mitigationplan=data['mitigationplan'],
                                  contigencyplan=data['contigencyplan'],
                                  team=team, owner=user)
        risk.save()

    def __init__(self, risk=False, *largs, **kargs):
        vals = dict()

        if risk:
            vals["identificationdate"] = risk.identificationdate
            vals["riskdetail"] = risk.riskdetail
            vals["impact"] = risk.impact
            vals["category"] = risk.category
            vals["mitigationplan"] = risk.mitigationplan
            vals["contigencyplan"] = risk.contigencyplan
            vals["team"] = risk.team

        super(RiskManagementForm, self).__init__(initial=vals, *largs, **kargs)
