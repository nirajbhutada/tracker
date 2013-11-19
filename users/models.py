from django.db import models
from django.contrib.auth.models import User


class Employees(models.Model):
    user = models.ForeignKey(User, related_name="emp_user")
    lastname = models.CharField(max_length=60, blank=True)
    firstname = models.CharField(max_length=30, blank=True)
    tshirtsize = models.CharField(max_length=75, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    hiredate = models.DateField(null=True, blank=True)
    emergencycontactno = models.CharField(max_length=72, blank=True)
    extension = models.CharField(max_length=12, blank=True)
    email = models.CharField(max_length=135, blank=True)
    notes = models.TextField(db_column='Notes', blank=True)
    reportsto = models.ForeignKey(User, related_name="reports_to",
                    null=True, blank=True)
    food_preferance = models.CharField(max_length=36, blank=True)
    home_location = models.CharField(max_length=45, blank=True)

    class Meta:
        db_table = u'employees'

    def __unicode__(self):
        if self.firstname:
            return '%s %s' % (self.firstname, self.lastname)
        else:
            return '%s %s' % (self.user.first_name, self.user.last_name)


class Teams(models.Model):

    lead = models.ForeignKey(User)
    teamname = models.CharField(max_length=90, blank=True)

    class Meta:
        db_table = u'teams'

    def __unicode__(self):
        return '%s' % (self.teamname)


# we don't use below two models we need to delete them soon
class Userlevels(models.Model):
    userlevelname = models.CharField(max_length=150, db_column='UserLevelName')

    class Meta:
        db_table = u'userlevels'


class Userlevelpermissions(models.Model):

    tablename = models.CharField(max_length=150)
    permission = models.IntegerField()

    class Meta:
        db_table = u'userlevelpermissions'
