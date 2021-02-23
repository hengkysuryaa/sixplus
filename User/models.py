from django.db import models

# Create your models here.
class User(models.Model):
	username = models.CharField(max_length = 20, primary_key=True)
	password = models.CharField(max_length = 50)
	name = models.CharField(max_length = 50)


	def __str__(self):
		return self.username + self.name