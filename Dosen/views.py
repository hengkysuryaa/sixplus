from django.shortcuts import render
from django.views import generic
from LO.models import *
from Dosen.models import Lecturer, Teaches, BobotIndeks
from User.views import *
from django.contrib.auth.models import User
from Utils.xlsxutil import export_pandas_to_sheet, convert_normal_array_to_pandas, import_workbook_as_pandasDict, import_sheet_as_pandas
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages

from User.decorators import authenticated_user

# Konstanta
komponen_nilai_list = ["uts1", "uts2", "uas", "kuis", "tutorial"]
indeks_list = ["A", "AB", "B", "BC", "C", "D", "E"]

# Create your views here.
######################
### HOMEPAGE DOSEN ###
######################

@authenticated_user
def HomepageDosenView(request, nip):
    return render(request, 'Dosen/dosen.html', {'nip' : nip})

##########################
### SECTION NAVIGATION ###
##########################

@authenticated_user
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
        print(section_list)
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

@authenticated_user
def SectionPage(request, nip, year, semester):
    #TO DO : Implementasi halaman untuk setiap kelas, ini termasuk upload dan download xlsx nilai
    if(request.method == 'POST'):
        section = request.POST.get('section')
        section_info = section.split(', ')
        course_id = section_info[0][0:6]
        section_id = section_info[-1]

    return redirect('dosen:SectionPage', nip = nip, year = year, semester = semester, course_id = course_id, section_id = section_id)

@authenticated_user
def SectionPage2(request, nip):
    if(request.method == 'POST'):
        section = request.POST.get('section')
        section_info = section.split(', ')
        year = section_info[0]
        semester = section_info[1]
        course_id = section_info[2][0:6]
        section_id = section_info[-1]

    return redirect('dosen:SectionPage', nip = nip, year = year, semester = semester, course_id = course_id, section_id = section_id)
######################
### KOMPONEN NILAI ###
######################

@authenticated_user
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

@authenticated_user
def FormsDistribusiNilai(request, nip, course_id):
    lo_list, course = LO.getCourseLO(LO, course_id)
    return render(request, 'Dosen/lo_form.html', {'list' : lo_list, 'nip' : nip, 'course' : course})

@authenticated_user
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
    return render(request, 'Dosen/berhasil.html', {'nip' : nip})


@authenticated_user
def penilaianPage(request, nip, year, semester, course_id, section_id):
    username = User.objects.filter(username = request.user.username)
    lecturer = Lecturer.objects.get(user = username[0])

    course = Course.objects.filter(course_id = course_id)[0]
    section = Section.objects.filter(course_id = course, sec_id = section_id, semester = semester, year = year)[0]
    
    student_list = Takes.objects.filter(section = section).values_list('student', flat = True)

    score_list = Score.getStudentTakesScores(Score, course_id = course_id, year = year, semester = semester, section_id = section_id)
    bobotindeks = BobotIndeks.objects.filter(section=section)
    if (len(score_list) != 0 and len(bobotindeks) !=0):
        calculateNilaiAkhir(year, semester, course_id, section_id)

    ##score_list = Score.objects.filter(nim__in = student_list, course = course)

    header = str(course_id) + " " + course.title +  " K" + str(section_id) + " Semester " + str(semester) + " " + str(year) + "-" + str(int(year)+1)

    #context = {'dosen' : lecturer}, 'section': sections, 'scores': scores}
    context = {'dosen' : lecturer , 'nip' : nip, 'year' : year, 'semester': semester, 'course_id' :course_id, 'section_id' : section_id, 'scores' : score_list, 'header' : header}
    return render(request, 'Dosen/penilaian.html', context)

@authenticated_user
def showPenilaianPage(request, nip):
    # print(request.POST.get('section'))
    username = User.objects.filter(username = request.user.username)
    lecturer = Lecturer.objects.get(user = username[0])
    lecturerForTeaches = Lecturer.objects.filter(user = username[0])
    teaches = Teaches.objects.filter(dosen = lecturerForTeaches[0])
    

    # # course = Course.objects.filter(course_id = course_id)[0]
    # section = Section.objects.filter(course_id = course, sec_id = section_id, semester = semester, year = year)[0]
    
    # student_list = Takes.objects.filter(section = section).values_list('student', flat = True)

    # score_list = Score.objects.filter(nim__in = student_list, course = course)

    # header = str(course_id) + " " + course.title +  " K" + str(section_id) + " Semester " + str(semester) + " " + str(year) + "-" + str(int(year)+1)

    #context = {'dosen' : lecturer}, 'section': sections, 'scores': scores}
    context = {'dosen' : lecturer , 'nip' : nip, 'teaches' : teaches}
    return render(request, 'Dosen/penilaian_teaches.html', context)

@authenticated_user
def exportListMhs(request, nip, year, semester, course_id, section_id):
    course = Course.objects.filter(course_id = course_id)[0]
    section = Section.objects.filter(course_id = course, sec_id = section_id, semester = semester, year = year)[0]
    list_nim, list_nama = Takes.get_student_takes(Takes, section)
    
    score_list = Score.getStudentTakesScores(Score, course_id = course_id, year = year, semester = semester, section_id = section_id)

    data = {'NIM':list_nim, 'Nama':list_nama, 'UTS1':[], 'UTS2':[], 'UAS':[], 'Kuis':[], 'Tutorial':[]}
    #data = {'NIM':[], 'Nama':[], 'UTS1':[], 'UTS2':[], 'UAS':[], 'Kuis':[], 'Tutorial':[]}

    for nim in list_nim:
        score = score_list.filter(takes__student__nim = nim)
        if(len(score) != 0):      
            data['UTS1'].append(score[0].uts1)
            data['UTS2'].append(score[0].uts2)
            data['UAS'].append(score[0].uas)
            data['Kuis'].append(score[0].kuis)
            data['Tutorial'].append(score[0].tutorial)
        else:
            data['UTS1'].append('')
            data['UTS2'].append('')
            data['UAS'].append('')
            data['Kuis'].append('')
            data['Tutorial'].append('')


    #data = {'NIM':list_nim, 'Nama':list_nama, 'UTS1':[], 'UTS2':[], 'UAS':[], 'Kuis':[], 'Tutorial':[]}
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

@authenticated_user
def FormsImportNilai(request, course_id):
    lo_list, course = LO.getCourseLO(LO, course_id)
    return render(request, 'Dosen/import.html', {'course' : course})

@authenticated_user
def checkScores(scores):
    for score in scores:
        if(score < 0 or score > 100):
            return False
    return True

@authenticated_user
def importListMhs(request, nip, year, semester, course_id, section_id):
    try:
        excel_file = request.FILES['excelUpload']
    except MultiValueDictKeyError:
        messages.error(request, 'NO DOCUMENT UPLOADED')
        return redirect('dosen:SectionPage', nip = nip, year = year, semester = semester, course_id = course_id, section_id = section_id)

    filename = str(excel_file).split('.')
    if(filename[-1] == "xlsx"):
        if(filename[0] == "Lembar Penilaian " + str(course_id) + " K" + str(section_id) + " Semester " + str(semester) + " " + str(year) + "-" + str(int(year)+1)):    
            dc = import_sheet_as_pandas(excel_file, str(course_id) + " K" + str(section_id) + " Semester " + str(semester) + " " + str(year) + "-" + str(int(year)+1))
            print(dc)
            for row in dc.itertuples():
                if(checkScores([row.UTS1, row.UTS2, row.UAS, row.Kuis, row.Tutorial])):
                    Score.setStudentScore(Score, row.NIM, course_id, year, semester, section_id, row.UTS1, row.UTS2, row.UAS, row.Kuis, row.Tutorial)
                    print(row.NIM, row.Nama, row.UTS1, row.UTS2, row.UAS, row.Kuis, row.Tutorial)
        else:
            messages.error(request, 'FILENAME IS WRONG, PLEASE CHECK THE NAME ONCE AGAIN')
    else:
        messages.error(request, 'FILE FORMAT NOT SUPPORTED')

    return redirect('dosen:SectionPage', nip = nip, year = year, semester = semester, course_id = course_id, section_id = section_id)
 
@authenticated_user   
def BobotIndeksView(request, nip, year, semester, course_id, section_id):
    
    #Ambil data
    section = Section.objects.filter(course__course_id = course_id, sec_id=section_id, semester=semester, year=year)
    bobotindeks = BobotIndeks.objects.filter(section=section[0])

    komponen_dict = {}
    for i in range(len(komponen_nilai_list)):
        if (len(bobotindeks) != 0):
            komponen_dict[komponen_nilai_list[i]] = bobotindeks[0].listbobot[i]
        else:
            komponen_dict[komponen_nilai_list[i]] = ''

    batas_indeks_dict = {}
    for i in range(len(indeks_list)):
        if (len(bobotindeks) != 0):
            batas_indeks_dict[indeks_list[i]] = bobotindeks[0].batasindeks[i]
        else:
           batas_indeks_dict[indeks_list[i]] = '' 

    return render(request, 'Dosen/bobot_indeks.html', {'nip':nip, 'year':year, 'semester':semester, 'course_id':course_id, 'section_id':section_id, 'section':section[0], 'batas_dict':batas_indeks_dict, 'komponen_dict':komponen_dict})

@authenticated_user
def BobotIndeksSubmitView(request, nip, year, semester, course_id, section_id):
    
    #Ambil data
    section = Section.objects.filter(course__course_id = course_id, sec_id=section_id, semester=semester, year=year)
    bobotindeks = BobotIndeks.objects.filter(section=section[0])

    listbobot = []
    sum = 0
    for i in range(len(komponen_nilai_list)):
        listbobot.append(int(request.POST[komponen_nilai_list[i]]))
        sum = sum + int(request.POST[komponen_nilai_list[i]])
    
    batasindeks = []
    for i in range(len(indeks_list)):
        batasindeks.append(int(request.POST[indeks_list[i]]))

    if (sum > 100):
        messages.error(request, 'Lebih Dari 100%. Silakan isi kembali')
    else:
        if (len(bobotindeks) != 0):
            BobotIndeks.objects.filter(section=section[0]).update(listbobot=listbobot, batasindeks=batasindeks)
        else:
            bi = BobotIndeks(section=section[0], listbobot=listbobot, batasindeks=batasindeks)
            bi.save()  
        calculateNilaiAkhir(year, semester, course_id, section_id)

    return redirect('dosen:SectionPage', nip = nip, year = year, semester = semester, course_id = course_id, section_id = section_id)    

@authenticated_user
def calculateNilaiAkhir(year, semester, course_id, section_id):
    section = Section.objects.filter(course__course_id = course_id, sec_id=section_id, semester=semester, year=year)
    takes = list(Takes.objects.filter(section=section[0]))
    bobotindeks = list(BobotIndeks.objects.filter(section=section[0]).values())[0].get('listbobot')
    batas_indeks_list = list(BobotIndeks.objects.filter(section=section[0]).values())[0].get('batasindeks')

    for i in range(len(takes)):
        score = list(Score.objects.filter(takes__student = takes[i].student, takes__section = takes[i].section).values())
        sum = 0
        for j in range(len(komponen_nilai_list)):
            sum = sum + (score[0].get(komponen_nilai_list[j]) * bobotindeks[j]) / 100
        
        indeks = '-'
        # Mapping sum ke indeks
        for k in range(len(indeks_list)):
            if (sum >= float(batas_indeks_list[k]) and sum <= float(100)):
                indeks = indeks_list[k]
                break
            elif (sum >= float(batas_indeks_list[k]) and sum < float(batas_indeks_list[k-1])):
                indeks = indeks_list[k]
                break
        
        Takes.objects.filter(student=takes[i].student, section=section[0]).update(grade=indeks)

def TestView(request, nip):
    print(nip)
    return render(request, 'Dosen/test.html', {'nip' : nip})

class TestClassView(generic.ListView):
    template_name = 'Dosen/test.html'
    nip = '14518390'

    def get_queryset(self):
        object_list = self.kwargs['nip']
        return self.kwargs['nip']
