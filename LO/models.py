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

class Score(models.Model):
    nim = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    uts1 = models.IntegerField()
    uts2 = models.IntegerField()
    uas = models.IntegerField()
    kuis = models.IntegerField()
    tutorial = models.IntegerField()

    def __str__(self):
        return f"{self.nim}, {self.course}, UTS1:{self.uts1}, UTS2:{self.uts2}, UAS:{self.uas}, Kuis:{self.kuis}, Tutorial:{self.tutorial}"

    def getStudentScore(self, nim, course_id):
        return Score.objects.filter(nim__nim=nim, course__course_id=course_id)

    def setStudentScore(self, nim, course_id, nilai_uts1, nilai_uts2, nilai_uas, nilai_kuis, nilai_tutorial):
        course = Course.objects.filter(course_id=course_id)[0]
        student = Student.objects.filter(nim=nim)[0]
        new_score = Score.objects.create(nim=student, course=course, uts1=nilai_uts1, uts2=nilai_uts2, uas=nilai_uas, kuis=nilai_kuis, tutorial=nilai_tutorial)
        return new_score

class BobotKomponenScore(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    uts1 = ArrayField(models.IntegerField())
    uts2 = ArrayField(models.IntegerField())
    uas = ArrayField(models.IntegerField())
    kuis = ArrayField(models.IntegerField())
    tutorial = ArrayField(models.IntegerField())
