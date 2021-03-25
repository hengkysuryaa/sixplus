from django.test import TestCase

# Create your tests here.
from LO.models import LO, Course, BobotKomponenScore, Takes, Section, Score
from Mahasiswa.models import Student


class ScoreViewTestCase(TestCase):
    def test_addScore(self):
    	Course.objects.create(course_id='MS1200', title='Test', dept_name = "FTMD", credits = 3)
    	Student.objects.create(nim='13518001', name='Johny', dept_name = "FTMD", total_credits = 3)
    	Student.objects.create(nim='13518002', name='Doe', dept_name = "FTMD", total_credits = 3)

    	student = Student.objects.filter(nim='13518001')[0]
    	self.assertTrue(student)

    	Score.setStudentScore(Score, '13518001', 'MS1200', 99, 99, 99, 99, 99)
    	Score.setStudentScore(Score, '13518002', 'MS1200', 100, 100, 100, 100, 100)	
    	self.assertTrue(Score.objects.filter(nim_id = 13518001))
    	self.assertTrue(Score.objects.filter(nim_id = 13518002))

