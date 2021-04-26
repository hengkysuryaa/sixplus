from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from LO.models import Section

# Create your models here.
class Lecturer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null = True)
	nip = models.CharField(max_length = 20, primary_key=True)
	name = models.CharField(max_length = 50)
	dept_name = models.CharField(max_length = 10)

	def __str__(self):
		return self.nip + " "+ self.name

class Teaches(models.Model):
	dosen = models.ForeignKey(Lecturer, on_delete=models.CASCADE, null = True)
	section = models.ForeignKey(Section, on_delete=models.CASCADE, null = True)

	def __str__(self):
		return f"{self.dosen} --- {self.section}"

class BobotIndeks(models.Model):
	section = models.ForeignKey(Section, on_delete=models.CASCADE)
	listbobot = ArrayField(models.IntegerField())
	batasindeks = ArrayField(models.IntegerField())
	
	def __str__(self):
		return f"{self.section}, Bobot: {self.listbobot}, Batas Indeks: {self.batasindeks}"