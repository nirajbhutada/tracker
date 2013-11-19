from django.db import models

'''
Need to work on active flag so instead of dete we can deactive so user data
will not end up showing error
'''


class ReleasePhase(models.Model):

    release_phase = models.CharField(max_length=90, blank=True)
    active = models.BooleanField()

    class Meta:
        db_table = u'releasephase'

    def __unicode__(self):
        return '%s' % self.release_phase


class Release(models.Model):

    relname = models.CharField(max_length=90, blank=True)
    active = models.BooleanField()

    class Meta:
        db_table = u'release'

    def __unicode__(self):
        return '%s' % self.relname





