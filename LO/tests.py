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

        # #Create response instance
        # res = ResponseKerjasama(student=student, course=course, Kontribusi=1, PemecahanMasalah=2, Sikap=3, FokusTerhadapTugas=4, BekerjaDenganOrangLain=3)
        # res.save()
        # #Checking
        # response = ResponseKerjasama.objects.filter(student=student, course=course)[0]
        # self.assertTrue(response)
