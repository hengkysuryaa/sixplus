from django.test import TestCase
from LO.models import LO, Course, BobotKomponenScore, Takes, Section, Score, ResponseKerjasama
from Mahasiswa.models import Student

# Create your tests here.

class ResponseKerjasama(TestCase):
    def test_addResponse(self):
        #Create course and student
        Course.objects.create(course_id='MS1200', title='Test', dept_name = "FTMD", credits = 3)
        Student.objects.create(nim='13518001', name='Johny', dept_name = "FTMD", total_credits = 3)
        #Checking
        course = Course.objects.filter(course_id='MS1200')[0]
        self.assertTrue(course)
        student = Student.objects.filter(nim='13518001')[0]
        self.assertTrue(student)