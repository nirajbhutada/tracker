'''
Created on 20-Jun-2012

@author: vijay
'''

from datetime import datetime
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth.models import User
from riskmanagement.forms import widgets

from users.models import Teams
from users.models import Userlevels
from users.models import Employees


class ChangePwdForm(forms.Form):
    old_password = forms.CharField(label="Current Password",
                    required=True,
                    widget=forms.widgets.PasswordInput,
                    error_messages={'required': (u'Old Password is required')})
    new_password = forms.CharField(label="New Password",
                    required=True,
                    widget=forms.widgets.PasswordInput,
                    error_messages={'required': (u'New Password is required')})
    confirm_password = forms.CharField(label="Confirm password",
                    required=True,
                    widget=forms.widgets.PasswordInput,
                error_messages={'required': (u'Confirm Password is required')})

    def clean_confirm_password(self):
        password0 = self.cleaned_data.get("new_password", "")
        password1 = self.cleaned_data["confirm_password"]
        if password0 != password1:
            raise forms.ValidationError("The two password fields didn't match.")
        if len(password0) < 4:
            raise forms.ValidationError("New Password length should be 4.")
        return password1


class TeamForm(forms.Form):
    teamname = forms.CharField(max_length=90, label='Team Name', required=True)

    def handle(self, data, team=None):
        "Handle submission of releases form"
        if team:
            lead = User.objects.get(id=data['lead'])
            team.lead = lead
            team.teamname = data['teamname']
        else:
            lead = User.objects.get(id=data['lead'])
            team = Teams(lead=lead, teamname=data['teamname'])
        team.save()

    def __init__(self, team=False, *largs, **kargs):
        vals = dict()
        if team:
            vals["teamname"] = team.teamname
            lead = widgets.UnValidatedChoiceField(label="Lead Name",
                    initial=team.lead.id,
                    choices=[(x.id, x.username) for x in User.objects.all()
                                if ((x.groups.filter(name="managers") or x.groups.filter(name="leads")))])
        super(TeamForm, self).__init__(initial=vals, *largs, **kargs)
        if not team:
            lead = widgets.UnValidatedChoiceField(label="Lead Name",
                    choices=[(x.id, x.username) for x in User.objects.all()
                                if (x.groups.filter(name="managers") or x.groups.filter(name="leads"))])
        self.fields.insert(2, 'lead', lead)


class EmployeeForm(forms.Form):
    firstname = forms.CharField(max_length=90, label='First Name', required=True)
    lastname = forms.CharField(max_length=90, label='Last Name', required=True)
    tshirtsize = forms.CharField(max_length=5, label='T-Shirt Size', required=True)
    birthdate = forms.DateField(label='Birth Date', required=False)
    hiredate = forms.DateField(label='Hire Date', required=False)
    emergencycontactno = forms.CharField(max_length=10,
                            label='Emergency Contact Number', required=True)
    extension = forms.CharField(max_length=12, label='Extension', required=False)
    email = forms.CharField(max_length=135, label='Email', required=True)
    notes = forms.CharField(widget=forms.Textarea, label='Notes', required=True)
    reportsto = forms.CharField(label='Manager/Lead', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    food_preferance = forms.CharField(max_length=36, label='Food Preference', required=False)
    home_location = forms.CharField(max_length=45, label='Home Location', required=True)

    def validators(self, data):
        flag = True
        if not data['birthdate']:
            self.errors['birthdate'] = "Birth Date field can't be empty"
            flag = False

        if not data['hiredate']:
            self.errors['hiredate'] = "Hire Date field can't be empty"
            flag = False
        return flag

    def handle(self, data, user=None, emp=None):
        "Handle submission of releases form"
        validated = self.validators(data)
        if validated:
            #reportsto = User.objects.get(id=data['reportsto'])
            birthdate = data['birthdate']
            hiredate = data['hiredate']
            if emp:
                emp.firstname = data['firstname']
                emp.lastname = data['lastname']
                emp.tshirtsize = data['tshirtsize']
                emp.birthdate = birthdate
                emp.hiredate = hiredate
                emp.emergencycontactno = data['emergencycontactno']
                emp.extension = data['extension']
                emp.email = data['email']
                emp.notes = data['notes']
#                emp.reportsto = reportsto
                emp.food_preferance = data['food_preferance']
                emp.home_location = data['home_location']
            else:
                emp = Employees(user=user, firstname=data['firstname'],
                                lastname=data['lastname'],
                                tshirtsize=data['tshirtsize'],
                                birthdate=birthdate,
                                hiredate=hiredate,
                                emergencycontactno=data['emergencycontactno'],
                                extension=data['extension'],
                                email=data['email'],
                                notes=data['notes'],
#                                reportsto=reportsto,

                                food_preferance=data['food_preferance'],
                                home_location=data['home_location'])
            emp.save()
            return True
        return False

    def __init__(self, emp=False, *largs, **kargs):
        vals = dict()

        if emp:
            vals['user'] = emp.user
            vals['firstname'] = emp.firstname
            vals['lastname'] = emp.lastname
            vals['tshirtsize'] = emp.tshirtsize
            vals['birthdate'] = emp.birthdate
            vals['hiredate'] = emp.hiredate
            vals['emergencycontactno'] = emp.emergencycontactno
            vals['extension'] = emp.extension
            vals['email'] = emp.email
            vals['notes'] = emp.notes
            vals['food_preferance'] = emp.food_preferance
            vals['home_location'] = emp.home_location
            if emp.reportsto:
                print 'reportsto : ', emp.reportsto
                vals['reportsto'] = emp.reportsto.first_name if emp.reportsto.first_name else emp.reportsto.username
            else:
                vals['reportsto'] = "You are not been assigned to a manager. Please contact your Manager for the same."
        super(EmployeeForm, self).__init__(initial=vals, *largs, **kargs)

#        reportsto = widgets.UnValidatedChoiceField(
#                        label="Manager/Lead",
#                        choices=[(x.id, '%s %s' % (x.first_name, x.last_name))
#                                 for x in User.objects.all().order_by('first_name', 'last_name')])
#        self.fields.insert(2, 'reportsto', reportsto)
