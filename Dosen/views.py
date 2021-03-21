from django.shortcuts import render
from django.views import generic
from LO.models import *
from Dosen.models import Lecturer
from User.views import *
from django.contrib.auth.models import User

# Create your views here.
class DistribusiKomponenNilaiView(generic.ListView):
    template_name = 'Dosen/page.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        bobot_list = BobotKomponenScore.objects.all()
        course_list = Course.objects.all()
        for items in bobot_list:
            print(items.course.course_id)
            course_list = course_list.exclude(course_id=items.course.course_id)
        
        return course_list

def FormsDistribusiNilai(request, course_id):
    lo_list, course = LO.getCourseLO(LO, course_id)
    return render(request, 'Dosen/lo_form.html', {'list' : lo_list, 'course' : course})

def SubmitView(request, course_id):
    # get all input values & convert to array of integer 
    uts1 = [int(numeric_str) for numeric_str in request.POST.getlist('uts1')]
    uts2 = [int(numeric_str) for numeric_str in request.POST.getlist('uts2')]
    uas = [int(numeric_str) for numeric_str in request.POST.getlist('uas')]
    kuis = [int(numeric_str) for numeric_str in request.POST.getlist('kuis')]
    tutorial = [int(numeric_str) for numeric_str in request.POST.getlist('tutorial')]
    course = Course.objects.filter(course_id = course_id)
    b = BobotKomponenScore(course=course[0], uts1=uts1, uts2=uts2, uas=uas, kuis=kuis, tutorial=tutorial)
    b.save()
    return render(request, 'Dosen/berhasil.html')

def penilaianPage(request):
    
    username = User.objects.filter(username = request.user.username)
    lecturer = Lecturer.objects.get(user = username[0])

    sections = Section.objects.all()
    scores = Score.objects.all()
    context = {'dosen' : lecturer, 'section': sections, 'scores': scores}
    return render(request, 'Dosen/penilaian.html', context)
