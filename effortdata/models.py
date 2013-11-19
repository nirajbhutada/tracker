from django.db import models
from users.models import Teams
from releasedata.models import Release, ReleasePhase
from django.contrib.auth.models import User
from users.models import Employees


class TaskType(models.Model):
    name = models.CharField(max_length=180, blank=False, null=False)

    class Meta:
        db_table = 'task_types'

    def __unicode__(self):
        return '%s' % self.name


class Target(models.Model):

    release = models.ForeignKey(Release, null=True, blank=True)
    release_phase = models.ForeignKey(ReleasePhase, null=True, blank=True)
    team = models.ForeignKey(Teams, null=True, blank=True)
    manualtcexectar = models.FloatField(null=True, blank=True)
    autotcexectar = models.FloatField(null=True, blank=True)
    prsveritar = models.FloatField(null=True, blank=True)
    tcwritar = models.FloatField(null=True, blank=True)
    completionpercentage = models.IntegerField(null=True, blank=True)
    emp = models.ForeignKey(User)
    updated_by = models.ForeignKey(User, null=False,
                 blank=False, related_name='target_updated_by')
    updated_datetime = models.DateField(null=False, blank=False)

    class Meta:
        db_table = u'target'


class Effortdata(models.Model):

    component = models.CharField(max_length=180, blank=True)
    product = models.CharField(max_length=90, blank=True)
    category = models.CharField(max_length=90, blank=True)
    prd_pmt_no = models.CharField(max_length=180, blank=True)
    testcasesplannedno = models.FloatField(null=True, blank=True)
    testcasesexecutedno = models.FloatField(null=True, blank=True)
    testcasesreexecutedno = models.FloatField(null=True, blank=True)
    taskdetail = models.TextField(blank=True)
    effort_date = models.DateField(null=True, blank=True)
    holiday = models.IntegerField(null=True, blank=True)
    prsplanned = models.FloatField(null=True, blank=True)
    prsverified = models.FloatField(null=True, blank=True)
    prsreproduced = models.FloatField(null=True, blank=True)
    prsfiled = models.FloatField(null=True, blank=True)
    issues_risks = models.TextField()
    tcexehr = models.IntegerField(null=True, blank=True)
    tcreexehr = models.IntegerField(null=True, blank=True)
    task_type = models.ForeignKey(TaskType)
    priorityoftc = models.CharField(max_length=30, blank=True)
    prsverhr = models.IntegerField(null=True, blank=True)
    prreprohrs = models.IntegerField(null=True, blank=True)
    tcdevelopmenthr = models.IntegerField(null=True, blank=True)
    prsfilehr = models.IntegerField(null=True, blank=True)
    traininghr = models.IntegerField(null=True, blank=True)
    meetconfhr = models.IntegerField(null=True, blank=True)
    qcportingtcno = models.IntegerField(null=True, blank=True)
    mischr = models.IntegerField(null=True, blank=True)

    planning = models.FloatField(null=True, blank=True)
    tcpassedno = models.FloatField(null=True, blank=True)
    tcfailedno = models.FloatField(null=True, blank=True)
    leaves = models.IntegerField(null=True, blank=True)
    tcdevelopednos = models.FloatField(null=True, blank=True)

    emp = models.ForeignKey(User)
    release = models.ForeignKey(Release)
    release_phase = models.ForeignKey(ReleasePhase)
    team = models.ForeignKey(Teams)
    updated_by = models.ForeignKey(User, null=False,
                     blank=False, related_name='updated_by')
    updated_datetime = models.DateField(null=False, blank=False)

    class Meta:
        db_table = u'effortdata'

    def __unicode__(self):
        return '%s,%s' % (self.product, self.testcasesplannedno)

    def user_profile(self):
        try:
            profile = Employees.objects.get(user=self.emp)
            if profile.firstname or profile.lastname:
                return  '%s %s' % (profile.firstname, profile.lastname)
            else:
                return  '%s %s' % (self.emp.first_name, self.emp.last_name)
        except Exception, e:
            print e
            if self.emp.first_name or self.emp.last_name:
                return  '%s %s' % (self.emp.first_name, self.emp.last_name)
            else:
                return self.emp.username


# looks like we don't use it need to delete in future
class IssueLog(models.Model):
    team = models.ForeignKey(Teams, null=True, blank=True)
    issuedetail = models.TextField(blank=True)
    issuepriority = models.CharField(max_length=36, blank=True)
    issuestatus = models.CharField(max_length=36, blank=True)
    reportedby = models.ForeignKey(User, related_name='issue_reported_by')
    closedby = models.ForeignKey(User, related_name='issue_closed_by')

    class Meta:
        db_table = u'issue_log'

# we don't use it so we need to delete in future
class Defectvalidity(models.Model):
    valid_date = models.DateField(null=True, blank=True)
    team = models.ForeignKey(Teams)
    release = models.ForeignKey(Release)
    release_phase = models.ForeignKey(ReleasePhase)
    total_defects = models.IntegerField(null=True, blank=True)
    dup_defects = models.IntegerField(null=True, blank=True)
    new_defects = models.IntegerField(null=True, blank=True)
    fixed_defects = models.IntegerField(null=True, blank=True)
    cosmic_defects = models.IntegerField(null=True, blank=True)
    obsol_defects = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = u'defectvalidity'

    def __unicode__(self):
        return '%s,%s,%s' % (self.release.relname, self.team.teamname,
                             self.total_defects)


