from django.db import models
from Mahasiswa.models import Student
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Course(models.Model):
    course_id = models.CharField(max_length=6, unique=True)
    title = models.CharField(max_length=100)
    dept_name = models.CharField(max_length=10)
    credits = models.IntegerField()

    def __str__(self):
        return f"{self.course_id} {self.title}"

class LO(models.Model):
    course_id = models.OneToOneField("Course", on_delete=models.CASCADE)
    lo_a = models.CharField(max_length=1)
    lo_b = models.CharField(max_length=1)
    lo_c = models.CharField(max_length=1)
    lo_d = models.CharField(max_length=1)
    lo_e = models.CharField(max_length=1)
    lo_f = models.CharField(max_length=1)
    lo_g = models.CharField(max_length=1)

    def __str__(self):
        return f"LO {self.course_id}"

class Section(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    sec_id = models.IntegerField(primary_key=True)
    semester = models.IntegerField()
    year = models.IntegerField()

    def __str__(self):
        return f"{self.course_id}, K{self.sec_id}, {self.semester}-{self.year}"

class Score(models.Model):
    nim = models.OneToOneField(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    uts1 = models.IntegerField()
    uts2 = models.IntegerField()
    uas = models.IntegerField()
    kuis = models.IntegerField()
    tutorial = models.IntegerField()

class BobotKomponenScore(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    uts1 = ArrayField(models.IntegerField())
    uts2 = ArrayField(models.IntegerField())
    uas = ArrayField(models.IntegerField())
    kuis = ArrayField(models.IntegerField())
    tutorial = ArrayField(models.IntegerField())