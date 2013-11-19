'''
Created on 21-Jun-2012

@author: vijay
'''

from datetime import datetime
from django import forms
from users.models import Teams
from releasedata.models import Release, ReleasePhase
from effortdata.models import TaskType, Effortdata
from riskmanagement.forms import widgets


class EffortForm(forms.Form):
    product = forms.CharField(label="Product", required=False,
                error_messages={'required': 'Product is Required'})
    category = forms.CharField(label="Category", required=False,
                error_messages={'required': 'Category is Required'})
    component = forms.CharField(label="Component", required=False,
                error_messages={'required': 'Component is Required'})
    taskdetail = forms.CharField(label="Task Details", required=True,
                widget=forms.Textarea,
                error_messages={'required': 'Task Details is Required'})
    effort_date = forms.DateField(label='Date', required=False,
                error_messages={'required': 'Date is Required'},
                input_formats=['%d-%m-%Y'])
    holiday = widgets.UnValidatedChoiceField(label="Holiday",
                choices=[(0, 'No'), (1, 'Yes')])
    leaves = forms.IntegerField(label="Leaves", required=True)
    prd_pmt_no = forms.CharField(label='PRD PMT No', required=True)

    testcasesplannedno = forms.FloatField(label='Planned', required=True,
                error_messages={
                    'required': "Test Cases Planned Nbr can't be empty",
                    'invalid': 'Test Cases Planned Nbr should be Float'
                })
    testcasesexecutedno = forms.FloatField(label='Executed', required=True,
                error_messages={
                    'required': "Test Cases Executed Nbr can't be empty"
                })
    testcasesreexecutedno = forms.FloatField(label='ReExecuted', required=True,
                error_messages={
                    'required': "Test Cases ReExecuted Nbr can't be empty"
                })

    tcpassedno = forms.FloatField(label='passed', required=True,
                error_messages={
                    'required': "Test Cases passed can't be empty"
                })
    tcfailedno = forms.FloatField(label='Failed', required=True,
                error_messages={
                    'required': "Test Cases Failed can't be empty"
                })
    tcdevelopednos = forms.FloatField(label='Developed', required=True,
                error_messages={
                    'required': "Test Cases Developed can't be empty"
                })
    tcexehr = forms.IntegerField(label='Execution', required=True,
                error_messages={
                    'required': "TC Executed Hours  can't be empty"
                })
    tcreexehr = forms.IntegerField(label='Reexecution', required=True,
                error_messages={
                    'required': "TC Reexecution Hours  can't be empty"
                })
    tcdevelopmenthr = forms.IntegerField(label='Development', required=True,
                 error_messages={
                    'required': "TC Development Hours  can't be empty"
                })

    prsplanned = forms.FloatField(label="Planned", required=True,
                error_messages={
                    'required': "Pr's Planned can't be empty"
                })
    prsverified = forms.FloatField(label="Verified", required=True,
                error_messages={
                    'required': "Pr's Verified can't be empty"
                })
    prsreproduced = forms.FloatField(label="Reproduced", required=True,
                 error_messages={
                    'required': "Pr's Reproduced can't be empty"
                })
    prsfiled = forms.FloatField(label="Filed", required=True,
                 error_messages={
                    'required': "Pr's Filed can't be empty"
                })

    issues_risks = forms.CharField(label="Issue/Risks", required=False,
                                   widget=forms.Textarea)
    prsverhr = forms.IntegerField(label="PRs Ver hrs", required=True,
                error_messages={
                 'required': "PRs Ver hrs can't be empty",
                 'invalid': 'PRs Ver hrs should be Integer'})

    prreprohrs = forms.IntegerField(label="PR Reproduce Hrs", required=True,
                error_messages={
                    'required': "PRs Reproduce hrs can't be empty",
                    'invalid': 'PR Reproduce Hrs should be Integer'
                    })
    prsfilehr = forms.IntegerField(label='PRs File Hrs', required=True,
                error_messages={
                     'required': "PRs File hrs can't be empty",
                    'invalid': 'PRs File Hrs should be Integer'
                })
    traininghr = forms.IntegerField(label='Training Hrs', required=True,
                error_messages={
                    'required': "Training hrs can't be empty",
                    'invalid': 'Training Hrs should be Integer'
                })
    meetconfhr = forms.IntegerField(label='Meet Conf Hrs', required=True,
                 error_messages={
                     'required': "Meet Conf Hrs can't be empty",
                     'invalid': 'Meet Conf Hrs should be Integer'
                })
    qcportingtcno = forms.IntegerField(label='TC QC Porting Nos', required=True,
                 error_messages={
                     'required': "TC QC Porting Nos can't be empty",
                     'invalid': 'TC QC Porting Nos should be Integer'
                })
    mischr = forms.IntegerField(label='Misc Hrs', required=False,
                 error_messages={
                     'required': "Misc hrs can't be empty",
                     'invalid': 'Misc Hrs should be Integer'
                })
    planning = forms.FloatField(label='Planning',)

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

    def clean_planning(self):
        self.check_int('leaves')

        self.check_float('testcasesplannedno')
        self.check_float('testcasesexecutedno')
        self.check_float('testcasesreexecutedno')
        self.check_float('tcpassedno')
        self.check_float('tcfailedno')
        self.check_float('tcdevelopednos')

        self.check_int('tcexehr')
        self.check_int('tcreexehr')
        self.check_int('tcdevelopmenthr')
        self.check_float('prsplanned')
        self.check_float('prsverified')
        self.check_float('prsreproduced')
        self.check_int('prsverhr')
        self.check_int('prreprohrs')
        self.check_int('prsfilehr')
        self.check_int('traininghr')
        self.check_int('meetconfhr')
        self.check_int('qcportingtcno')
        self.check_int('mischr')
        self.check_float('planning')

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
            raise forms.ValidationError('Releases is Required')

    def clean_release_phase(self):
        data = self.cleaned_data['release_phase']
        if int(data):
            return data
        else:
            raise forms.ValidationError('Phases is Required')

    def clean_task_type(self):
        data = self.cleaned_data['task_type']
        if int(data):
            return data
        else:
            raise forms.ValidationError('Tasks is Required')

    def handle(self, data, user=None, effort=None):
        "Handle submission of releases form"

        teamobj = Teams.objects.get(id=data['team'])
        release = Release.objects.get(id=data['release'])
        release_phase = ReleasePhase.objects.get(id=data['release_phase'])
        eff_date = datetime.strptime(data['effort_date'], '%d-%m-%Y')
        task_type = TaskType.objects.get(id=data['task_type'])
        if effort:
            effort.release = release
            effort.release_phase = release_phase
            effort.team = teamobj
            effort.product = data['product']
            effort.category = data['category']
            effort.component = data['component']
            effort.task_type = task_type
            effort.taskdetail = data['taskdetail']
            effort.effort_date = eff_date
            effort.holiday = data['holiday']
            effort.leaves = data['leaves']
            effort.prd_pmt_no = float(data['prd_pmt_no'])
            effort.testcasesplannedno = float(data['testcasesplannedno'])
            effort.testcasesexecutedno = float(data['testcasesexecutedno'])
            effort.testcasesreexecutedno = float(data['testcasesreexecutedno'])
            effort.tcpassedno = float(data['tcpassedno'])
            effort.tcfailedno = float(data['tcfailedno'])
            effort.tcdevelopednos = float(data['tcdevelopednos'])
            effort.tcexehr = float(data['tcexehr'])
            effort.tcreexehr = float(data['tcreexehr'])
            effort.tcdevelopmenthr = float(data['tcdevelopmenthr'])
            effort.prsplanned = float(data['prsplanned'])
            effort.prsverified = float(data['prsverified'])
            effort.prsreproduced = float(data['prsreproduced'])
            effort.prsfiled = float(data['prsfiled'])
            effort.issues_risks = data['issues_risks']
            effort.prsverhr = float(data['prsverhr'])
            effort.prreprohrs = float(data['prreprohrs'])
            effort.prsfilehr = float(data['prsfilehr'])
            effort.traininghr = float(data['traininghr'])
            effort.meetconfhr = float(data['meetconfhr'])
            effort.qcportingtcno = float(data['qcportingtcno'])
            effort.mischr = float(data['mischr'])
            effort.planning = float(data['planning'])
            effort.updated_by = user
            effort.updated_datetime = datetime.now()

        else:
            effort = Effortdata(emp=user,
                        release=release,
                        release_phase=release_phase,
                        team=teamobj,
                        product=data['product'],
                        category=data['category'],
                        component=data['component'],
                        task_type=task_type,
                        taskdetail=data['taskdetail'],
                        effort_date=eff_date,
                        holiday=data['holiday'],
                        leaves=data['leaves'],
                        prd_pmt_no=data['prd_pmt_no'],
                        testcasesplannedno=float(data['testcasesplannedno']),
                        testcasesexecutedno=float(data['testcasesexecutedno']),
                        testcasesreexecutedno=float(data['testcasesreexecutedno']),
                        tcpassedno=float(data['tcpassedno']),
                        tcfailedno=float(data['tcfailedno']),
                        tcdevelopednos=float(data['tcdevelopednos']),
                        tcexehr=float(data['tcexehr']),
                        tcreexehr=float(data['tcreexehr']),
                        tcdevelopmenthr=float(data['tcdevelopmenthr']),
                        prsplanned=float(data['prsplanned']),
                        prsverified=float(data['prsverified']),
                        prsreproduced=float(data['prsreproduced']),
                        prsfiled=float(data['prsfiled']),
                        issues_risks=data['issues_risks'],
#                                priorityoftc=data['priorityoftc'],
                        prsverhr=float(data['prsverhr']),
                        prreprohrs=float(data['prreprohrs']),
                        prsfilehr=float(data['prsfilehr']),
                        traininghr=float(data['traininghr']),
                        meetconfhr=float(data['meetconfhr']),
                        qcportingtcno=float(data['qcportingtcno']),
                        mischr=float(data['mischr']),
                        planning=float(data['planning']),
                        updated_by=user,
                        updated_datetime=datetime.now())
        effort.save()

    def __init__(self, effort=False, user=None, *largs, **kargs):
        vals = dict()
        if effort:
            eff_date = (effort.effort_date).strftime('%d-%m-%Y')
            vals['effort_date'] = eff_date
            vals['holiday'] = effort.holiday
            vals['testcasesplannedno'] = effort.testcasesplannedno
            vals['testcasesexecutedno'] = effort.testcasesexecutedno
            vals['testcasesreexecutedno'] = effort.testcasesreexecutedno
            vals['taskdetail'] = effort.taskdetail if effort.taskdetail else ''
            vals['component'] = effort.component
            vals['product'] = effort.product
            vals['category'] = effort.category
            vals['prd_pmt_no'] = effort.prd_pmt_no
            vals['prsplanned'] = effort.prsplanned
            vals['prsverified'] = effort.prsverified
            vals['prsreproduced'] = effort.prsreproduced
            vals['prsfiled'] = effort.prsfiled
            vals['issues_risks'] = effort.issues_risks if effort.issues_risks else ''
            vals['tcexehr'] = effort.tcexehr
            vals['tcreexehr'] = effort.tcreexehr
            vals['prsverhr'] = effort.prsverhr
            vals['prreprohrs'] = effort.prreprohrs
            vals['tcdevelopmenthr'] = effort.tcdevelopmenthr
            vals['prsfilehr'] = effort.prsfilehr
            vals['traininghr'] = effort.traininghr
            vals['meetconfhr'] = effort.meetconfhr
            vals['qcportingtcno'] = effort.qcportingtcno
            vals['mischr'] = effort.mischr
            vals['planning'] = effort.planning
            vals['tcpassedno'] = effort.tcpassedno
            vals['tcfailedno'] = effort.tcfailedno
            vals['leaves'] = effort.leaves
            vals['tcdevelopednos'] = effort.tcdevelopednos
            vals['team'] = effort.team.id
            vals['task_type'] = effort.task_type.id
            vals['release'] = effort.release.id
            vals['release_phase'] = effort.release_phase.id

        else:
            vals['testcasesplannedno'] = 0
            vals['testcasesexecutedno'] = 0
            vals['testcasesreexecutedno'] = 0
            vals['prd_pmt_no'] = 0
            vals['prsplanned'] = 0
            vals['prsverified'] = 0
            vals['prsreproduced'] = 0
            vals['leaves'] = 0
            vals['prsfiled'] = 0
            vals['tcexehr'] = 0
            vals['tcreexehr'] = 0
            vals['tcpassedno'] = 0
            vals['tcfailedno'] = 0
            vals['tcdevelopednos'] = 0
            vals['prsverhr'] = 0
            vals['prreprohrs'] = 0
            vals['tcdevelopmenthr'] = 0
            vals['prsfilehr'] = 0
            vals['traininghr'] = 0
            vals['meetconfhr'] = 0
            vals['qcportingtcno'] = 0
            vals['mischr'] = 0
            vals['planning'] = 0
            vals['taskdetail'] = ''
            vals['issues_risks'] = ''
            vals['effort_date'] = datetime.today().strftime('%d-%m-%Y')

        super(EffortForm, self).__init__(initial=vals, *largs, **kargs)
        choices = [[0, 'Select One']]
        choices.extend([[x.id, x.relname] for x in Release.objects.all()])
        release = widgets.UnValidatedChoiceField(label="Releases",
            choices=choices, required=True,
            error_messages={'required': 'Releases is Required'})

        choices = [[0, 'Select One']]
        choices.extend([[x.id, x.teamname] for x in Teams.objects.all()])
        team = widgets.UnValidatedChoiceField(label="Team",
                     choices=choices, required=True,
                     error_messages={'required': 'Team is Required'})

        choices = [[0, 'Select One']]
        choices.extend([[x.id, x.name] for x in TaskType.objects.all()])
        task_type = widgets.UnValidatedChoiceField(label="Tasks",
                                                   choices=choices,
                                                   required=True,
                                                   error_messages={'required':'Tasks is Required'})

        choices = [[0, 'Select One']]
        choices.extend([(x.id, x.release_phase)
                                 for x in ReleasePhase.objects.all()])
        release_phase = widgets.UnValidatedChoiceField(label="Phases",
                                                       choices=choices,
                                                       required=True,
                                                       error_messages={'required':'Phases is Required'})
        self.fields.insert(2, 'release', release)
        self.fields.insert(3, 'release_phase', release_phase)
        self.fields.insert(4, 'team', team)
        self.fields.insert(5, 'task_type', task_type)
