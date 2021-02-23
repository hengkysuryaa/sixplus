from django.db import models

# Create your models here.
class Student(models.Model):
	nim = models.CharField(max_length = 10, primary_key=True)
	name = models.CharField(max_length = 50)
	dept_name = models.CharField(max_length = 10)
	total_credits = models.IntegerField(default = 0)

	def __str__(self):
		return self.nim + self.name
