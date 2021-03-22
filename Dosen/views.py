from django.shortcuts import render
from django.views import generic
from LO.models import *
from Dosen.models import Lecturer
from User.views import *
from django.contrib.auth.models import User
from Utils.xlsxutil import export_pandas_to_sheet, convert_normal_array_to_pandas, import_workbook_as_pandasDict, import_sheet_as_pandas
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.
class DistribusiKomponenNilaiView(generic.ListView):
    template_name = 'Dosen/page.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        bobot_list = BobotKomponenScore.objects.all()
        course_list = Course.objects.all().order_by('course_id')
        for items in bobot_list:
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

<<<<<<< Dosen/views.py
def penilaianPage(request):
    
    username = User.objects.filter(username = request.user.username)
    lecturer = Lecturer.objects.get(user = username[0])

    sections = Section.objects.all()
    scores = Score.objects.all()
    context = {'dosen' : lecturer, 'section': sections, 'scores': scores}
    return render(request, 'Dosen/penilaian.html', context)
=======
def downloadListMhs(section):
    list_nim, list_nama = Takes.get_student_takes(Takes, section)
    data = {'NIM':list_nim, 'Nama':list_nama, 'UTS1':[], 'UTS2':[], 'UAS':[], 'Kuis':[], 'Tutorial':[]}
    df = convert_normal_array_to_pandas(data)
    name = section.course_id.course_id + " K" + str(section.sec_id)

    export_pandas_to_sheet(df, "Lembar Penilaian " + name + ".xlsx", name)

def exportListMhs(request, course_id):
    #list_nim, list_nama = Takes.get_student_takes(Takes, section)
    list_nim = ['13518103', '13518114']
    list_nama = ['Gunawan', 'Kamaruddin']
    data = {'NIM':list_nim, 'Nama':list_nama, 'UTS1':[], 'UTS2':[], 'UAS':[], 'Kuis':[], 'Tutorial':[]}
    df = convert_normal_array_to_pandas(data)
    #name = section.course_id.course_id + " K" + str(section.sec_id)
    name = "MS1210" + "K5"

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename=Lembar Penilaian {name}.xlsx'.format(
        name = name,
    )

    export_pandas_to_sheet(df, response, name)

    return response

def FormsImportNilai(request, course_id):
    lo_list, course = LO.getCourseLO(LO, course_id)
    return render(request, 'Dosen/import.html', {'course' : course})

def importListMhs(request, course_id):
    lo_list, course = LO.getCourseLO(LO, course_id)
    try:
        excel_file = request.FILES['fileToUpload']
    except MultiValueDictKeyError:
        return render(request, 'Dosen/import.html', {'course' : course})

    filename = str(excel_file).split('.')
    if(filename[-1] == "xlsx"):
        dc = import_sheet_as_pandas(excel_file, ' '.join((filename[0].split(' ')[2], filename[0].split(' ')[3])))
        print(dc)
        for row in dc.itertuples():
            Score.setStudentScore(Score, row.NIM, course_id, row.UTS1, row.UTS2, row.UAS, row.Kuis, row.Tutorial)
            print(row.NIM, row.Nama, row.UTS1, row.UTS2, row.UAS, row.Kuis, row.Tutorial)

        for row in dc.itertuples():
            print(Score.getStudentScore(Score, row.NIM, course_id).uts1)

    return render(request, 'Dosen/berhasil.html')
>>>>>>> Dosen/views.py
