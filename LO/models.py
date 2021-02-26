from django.db import models
from Mahasiswa.models import Student

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

class Takes(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, default=0)
    grade = models.CharField(default='-', max_length=2)

    def __str__(self):
        return f"{self.student}, {self.section}, {self.grade}"
    
    def get_student_takes(self, Section):
        t = Takes.objects.filter(section = Section)
        student_list = []
        for obj in t:
            student_list.append(obj.student)
        return student_list