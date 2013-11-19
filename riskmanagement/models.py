from django.db import models
from users.models import Teams
from django.contrib.auth.models import User
# Create your models here.


# Need to discuss if we need them for futire use

class RiskManagement(models.Model):
    identificationdate = models.DateField(null=True, blank=True)
    team = models.ForeignKey(Teams, null=True, blank=True)
    owner = models.ForeignKey(User)
    riskdetail = models.TextField(blank=True)
    category = models.CharField(max_length=36, blank=True)
    impact = models.CharField(max_length=36, blank=True)
    mitigationplan = models.TextField(blank=True)
    contigencyplan = models.TextField()

    class Meta:
        db_table = u'risk_management'
