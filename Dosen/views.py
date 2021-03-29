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
######################
### HOMEPAGE DOSEN ###
######################
def HomepageDosenView(request, nip):
    # TO DO : Make Dosen's Homepage
    return render(request, 'Dosen/test.html', {'nip' : nip}) # Placeholder code

##########################
### SECTION NAVIGATION ###
##########################
class DosenSectionListView(generic.ListView):
    # TO DO : RENDER SECTIONS FOR SEMESTER AND YEAR
    template_name = 'Dosen/section_list.html' # Placeholder
    context_object_name = 'section_list'
    

    def get_queryset(self):
        # Get the sections you want to show here
        # nip = self.kwargs['nip']
        # year = self.kwargs['year']
        # semester = self.kwargs['semester']

        section_list = Section.objects.filter(semester = self.kwargs['semester'], year = self.kwargs['year'])
        
        return section_list

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Add in a QuerySet of all the context
        username = User.objects.filter(username = self.request.user.username)
        lecturer = Lecturer.objects.get(user = username[0])

        context['dosen'] = lecturer
        context['nip'] = self.kwargs['nip']
        context['year'] = self.kwargs['year']
        context['semester'] = self.kwargs['semester']
        return context

def SectionPage(request, nip, year, semester):
    #TO DO : Implementasi halaman untuk setiap kelas, ini termasuk upload dan download xlsx nilai
    if(request.method == 'POST'):
        section = request.POST.get('section')
        course_id = section[0:6]
        section_id = section[-1]

    return redirect('dosen:SectionPage', nip = nip, year = year, semester = semester, course_id = course_id, section_id = section_id)

######################
### KOMPONEN NILAI ###
######################
class DistribusiKomponenNilaiView(generic.ListView):
    template_name = 'Dosen/page.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        bobot_list = BobotKomponenScore.objects.all()
        course_list = Course.objects.all().order_by('course_id')
        for items in bobot_list:
            course_list = course_list.exclude(course_id=items.course.course_id)
        
        return course_list

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        context['nip'] = self.kwargs['nip']
        return context

def FormsDistribusiNilai(request, nip, course_id):
    lo_list, course = LO.getCourseLO(LO, course_id)
    return render(request, 'Dosen/lo_form.html', {'list' : lo_list, 'nip' : nip, 'course' : course})

def SubmitView(request, nip, course_id):
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


def penilaianPage(request, nip, year, semester, course_id, section_id):
    username = User.objects.filter(username = request.user.username)
    lecturer = Lecturer.objects.get(user = username[0])

    course = Course.objects.filter(course_id = course_id)[0]
    section = Section.objects.filter(course_id = course, sec_id = section_id, semester = semester, year = year)[0]
    
    student_list = Takes.objects.filter(section = section).values_list('student', flat = True)

    score_list = Score.objects.filter(nim__in = student_list, course = course)

    header = str(course_id) + " " + course.title +  " K" + str(section_id) + " Semester " + str(semester) + " " + str(year) + "-" + str(int(year)+1)

    #context = {'dosen' : lecturer}, 'section': sections, 'scores': scores}
    context = {'dosen' : lecturer , 'nip' : nip, 'year' : year, 'semester': semester, 'course_id' :course_id, 'section_id' : section_id, 'scores' : score_list, 'header' : header}
    return render(request, 'Dosen/penilaian.html', context)

def showPenilaianPage(request, nip, year, semester):
    print(request.POST.get('section'))
    username = User.objects.filter(username = request.user.username)
    lecturer = Lecturer.objects.get(user = username[0])

    course = Course.objects.filter(course_id = course_id)[0]
    section = Section.objects.filter(course_id = course, sec_id = section_id, semester = semester, year = year)[0]
    
    student_list = Takes.objects.filter(section = section).values_list('student', flat = True)

    score_list = Score.objects.filter(nim__in = student_list, course = course)

    header = str(course_id) + " " + course.title +  " K" + str(section_id) + " Semester " + str(semester) + " " + str(year) + "-" + str(int(year)+1)

    #context = {'dosen' : lecturer}, 'section': sections, 'scores': scores}
    context = {'dosen' : lecturer , 'nip' : nip, 'year' : year, 'semester': semester, 'course_id' :course_id, 'section_id' : section_id, 'scores' : score_list, 'header' : header}
    return render(request, 'Dosen/penilaian.html', context)


def exportListMhs(request, nip, year, semester, course_id, section_id):
    course = Course.objects.filter(course_id = course_id)[0]
    section = Section.objects.filter(course_id = course, sec_id = section_id, semester = semester, year = year)[0]
    list_nim, list_nama = Takes.get_student_takes(Takes, section)
    data = {'NIM':list_nim, 'Nama':list_nama, 'UTS1':[], 'UTS2':[], 'UAS':[], 'Kuis':[], 'Tutorial':[]}
    df = convert_normal_array_to_pandas(data)
    #name = section.course_id.course_id + " K" + str(section.sec_id)
    name = str(course_id) + " K" + str(section_id) + " Semester " + str(semester) + " " + str(year) + "-" + str(int(year)+1)

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

def importListMhs(request, nip, year, semester, course_id, section_id):
    lo_list, course = LO.getCourseLO(LO, course_id)
    try:
        excel_file = request.FILES['excelUpload']
    except MultiValueDictKeyError:
        return redirect('dosen:SectionPage', nip = nip, year = year, semester = semester, course_id = course_id, section_id = section_id)

    filename = str(excel_file).split('.')
    if(filename[-1] == "xlsx"):
        if(filename[0] == "Lembar Penilaian " + str(course_id) + " K" + str(section_id) + " Semester " + str(semester) + " " + str(year) + "-" + str(int(year)+1)):    
            dc = import_sheet_as_pandas(excel_file, str(course_id) + " K" + str(section_id) + " Semester " + str(semester) + " " + str(year) + "-" + str(int(year)+1))
            print(dc)
        for row in dc.itertuples():
             Score.setStudentScore(Score, row.NIM, course_id, row.UTS1, row.UTS2, row.UAS, row.Kuis, row.Tutorial)
             print(row.NIM, row.Nama, row.UTS1, row.UTS2, row.UAS, row.Kuis, row.Tutorial)

    return redirect('dosen:SectionPage', nip = nip, year = year, semester = semester, course_id = course_id, section_id = section_id)
    

def TestView(request, nip):
    print(nip)
    return render(request, 'Dosen/test.html', {'nip' : nip})

class TestClassView(generic.ListView):
    template_name = 'Dosen/test.html'
    nip = '14518390'

    def get_queryset(self):
        object_list = self.kwargs['nip']
        return self.kwargs['nip']
