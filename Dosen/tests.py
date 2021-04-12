from django.test import TestCase

# Create your tests here.
from LO.models import LO, Course, BobotKomponenScore, Takes, Section, Score
from Mahasiswa.models import Student


class ScoreViewTestCase(TestCase):
    def test_addScore(self):
        course = Course.objects.create(course_id='MS1200', title='Test', dept_name = "FTMD", credits = 3)
        student1 = Student.objects.create(nim='13518001', name='Johny', dept_name = "FTMD", total_credits = 3)
        student2 = Student.objects.create(nim='13518002', name='Doe', dept_name = "FTMD", total_credits = 3)
        section = Section.objects.create(course = course, sec_id = 1, semester = 1, year = 2020)
        #section = Section.objects.create(course_id = 'MS1200', sec_id = 1, semester = 1, year = 2020)

        Takes.objects.create(student = student1, section = section)
        Takes.objects.create(student = student2, section = section)
        #Takes.objects.create(student = student1, section = section)
        #Takes.objects.create(student = student2, section = section)

        student = Student.objects.filter(nim='13518001')[0]
        self.assertTrue(student)

        Score.setStudentScore(Score, '13518001', 'MS1200', 2020, 1, 1, 99, 99, 99, 99, 99)
        Score.setStudentScore(Score, '13518002', 'MS1200', 2020, 1, 1, 100, 100, 100, 100, 100)	
        self.assertTrue(Score.objects.filter(takes__student__nim = 13518001))
        self.assertTrue(Score.objects.filter(takes__student__nim = 13518002))

