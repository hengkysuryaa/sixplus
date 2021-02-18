from django.db import models

# Create your models here.
class LO(models.Model):
    lo_a = models.CharField(max_length=1)
    lo_b = models.CharField(max_length=1)
    lo_c = models.CharField(max_length=1)
    lo_d = models.CharField(max_length=1)
    lo_e = models.CharField(max_length=1)
    lo_f = models.CharField(max_length=1)
