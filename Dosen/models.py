from django.db import models

# Create your models here.
class Lecturer(models.Model):
	nip = models.CharField(max_length = 20)
	name = models.CharField(max_length = 50)
	dept_name = models.CharField(max_length = 10)

	def __str__(self):
		return self.nip + self.name
