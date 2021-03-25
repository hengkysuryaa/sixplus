from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Lecturer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null = True)
	nip = models.CharField(max_length = 20, primary_key=True)
	name = models.CharField(max_length = 50)
	dept_name = models.CharField(max_length = 10)

	def __str__(self):
		return self.nip + self.name
