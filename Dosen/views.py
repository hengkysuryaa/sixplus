from django.shortcuts import render, get_object_or_404
from django.views import generic
from LO.models import *
from Dosen.models import Lecturer, Teaches, BobotIndeks
from User.views import *
from django.contrib.auth.models import User
from Utils.xlsxutil import export_pandas_to_sheet, convert_normal_array_to_pandas, import_workbook_as_pandasDict, import_sheet_as_pandas
from django.http import HttpResponse, HttpResponseNotFound
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages
from Mahasiswa.views import calculateLO
import numpy as np

from User.decorators import allowed_users


# Konstanta
komponen_nilai_list = ["uts1", "uts2", "uas", "kuis", "tutorial"]
indeks_list = ["A", "AB", "B", "BC", "C", "D", "E"]
lo_list = ['lo_a', 'lo_b', 'lo_c', 'lo_d', 'lo_e', 'lo_f', 'lo_g']
KMT = {
    "L" : 1,
    "M" : 2,
    "H" : 3
}

# Create your views here.
######################
### HOMEPAGE DOSEN ###
######################

@allowed_users(['dosen'])
def HomepageDosenView(request, nip):
    dosen = get_object_or_404(Lecturer, nip = nip)
    return render(request, 'Dosen/dosen.html', {'nip' : nip, 'dosen' : dosen})

##########################
### SECTION NAVIGATION ###
##########################

class DosenSectionListView(generic.ListView):
    # TO DO : RENDER SECTIONS FOR SEMESTER AND YEAR
    template_name = 'Dosen/section_list.html' # Placeholder
    context_object_name = 'section_list'
    
    
    # @allowed_users(['dosen'])
    def get_queryset(self):
        # Get the sections you want to show here
        # nip = self.kwargs['nip']
        # year = self.kwargs['year']
        # semester = self.kwargs['semester']

        section_list = Section.objects.filter(semester = self.kwargs['semester'], year = self.kwargs['year'])
        print(section_list)
        return section_list
    
    # @allowed_users(['dosen'])
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

@allowed_users(['dosen'])
def SectionPage(request, nip, year, semester):
    #TO DO : Implementasi halaman untuk setiap kelas, ini termasuk upload dan download xlsx nilai
    if(request.method == 'POST'):
        section = request.POST.get('section')
        section_info = section.split(', ')
        course_id = section_info[0][0:6]
        section_id = section_info[-1]

    return redirect('dosen:SectionPage', nip = nip, year = year, semester = semester, course_id = course_id, section_id = section_id)

@allowed_users(['dosen'])
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


class DistribusiKomponenNilaiView(generic.ListView):
    template_name = 'Dosen/page.html'
    context_object_name = 'course_list'

    # @allowed_users(['dosen'])
    def get_queryset(self):
        bobot_list = BobotKomponenScore.objects.all()
        course_list = Course.objects.all().order_by('course_id')
        for items in bobot_list:
            course_list = course_list.exclude(course_id=items.course.course_id)
        
        return course_list
    
    # @allowed_users(['dosen'])
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        context['nip'] = self.kwargs['nip']
        return context

@allowed_users(['dosen'])
def FormsDistribusiNilai(request, nip, course_id):
    lo_list, course = LO.getCourseLO(LO, course_id)
    return render(request, 'Dosen/lo_form.html', {'list' : lo_list, 'nip' : nip, 'course' : course})

@allowed_users(['dosen'])
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


@allowed_users(['dosen'])
def penilaianPage(request, nip, year, semester, course_id, section_id):
    count_indeks_dict = countIndeks(year, semester, course_id, section_id)

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
    context = {'indeks_dict' : count_indeks_dict, 'dosen' : lecturer , 'nip' : nip, 'year' : year, 'semester': semester, 'course_id' :course_id, 'section_id' : section_id, 'scores' : score_list, 'header' : header}
    return render(request, 'Dosen/penilaian.html', context)

@allowed_users(['dosen'])
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

@allowed_users(['dosen'])
def FormsImportNilai(request, course_id):
    lo_list, course = LO.getCourseLO(LO, course_id)
    return render(request, 'Dosen/import.html', {'course' : course})

def checkScores(scores):
    for score in scores:
        if(score < 0 or score > 100):
            return False
    return True

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
 
@allowed_users(['dosen'])
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

@allowed_users(['dosen'])
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

def calculateNilaiAkhir(year, semester, course_id, section_id):
    section = Section.objects.filter(course__course_id = course_id, sec_id=section_id, semester=semester, year=year)
    takes = list(Takes.objects.filter(section=section[0]))
    bobotindeks = list(BobotIndeks.objects.filter(section=section[0]).values())[0].get('listbobot')
    batas_indeks_list = list(BobotIndeks.objects.filter(section=section[0]).values())[0].get('batasindeks')

    for i in range(len(takes)):
        score = list(Score.objects.filter(takes__student = takes[i].student, takes__section = takes[i].section).values())
        
        if (len(score) == 0):
            break

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

def calculateCourseOutcomeLO(_course_id, _year, _semester):
    takes_list = list(Takes.objects.filter(section__year = _year, section__semester = _semester, section__course__course_id = _course_id))
    lo_sup_std_list = []
    for i in range (len(takes_list)):
        # Cek apakah nilai nya ada
        score = Score.objects.filter(takes=takes_list[i])
        if (len(score) > 0):
            lo_course = calculateLO(takes_list[i].student.nim, _course_id, _year, _semester)
            lo_sup_std_list.append(lo_course)
    
    course_outcome_dict = {}

    course_lo_list = list(LO.getCourseLO(LO, _course_id)[0].keys())

    for i in range (len(lo_list)):
        if (len(lo_sup_std_list) > 0):
            if (lo_list[i] in course_lo_list):
                sum = 0
                for j in range (len(lo_sup_std_list)):
                    sum = sum + float(lo_sup_std_list[j].get(lo_list[i]))
                course_outcome_dict[lo_list[i]] = round(sum/len(lo_sup_std_list), 2)
            else:
                course_outcome_dict[lo_list[i]] = '-'
        else:
            course_outcome_dict[lo_list[i]] = '-'

    course_outcome_dict["course"] = LO.getCourseLO(LO, _course_id)[1]
    if (len(lo_sup_std_list) == 0):
        course_outcome_dict["len_lo_sup_std"] = 0

    return course_outcome_dict

def calculateLOAssesment(_year, _semester):
    section_list = list(Section.objects.filter(year=_year, semester=_semester))
    course_list = []
    for item in section_list:
        course_list.append(item.course.course_id)
    course_list = sorted(list(set(course_list)))
    
    course_assessment_list = []
    for i in range(len(course_list)):
        course_assessment_list.append(calculateCourseOutcomeLO(course_list[i], _year, _semester))

    lo_assessment_dict = {}
    
    for i in range(len(lo_list)):
        sum = 0.0
        sum_divisor = 0.0
        for j in range(len(course_assessment_list)):
            if (course_assessment_list[j].get('len_lo_sup_std') == None):
                lo_course_dict = LO.getCourseLO(LO, course_assessment_list[j].get('course').course_id)[0]
                course_lo = list(lo_course_dict.keys())
                if (lo_list[i] in course_lo):
                    sum = sum + float(course_assessment_list[j].get(lo_list[i]) * KMT.get(lo_course_dict.get(lo_list[i])))
                    sum_divisor = sum_divisor + float(KMT.get(lo_course_dict.get(lo_list[i])))
        if (sum == 0.0 and sum_divisor == 0.0):
            lo_assessment_dict[lo_list[i]] = '-'
        else:
            lo_assessment_dict[lo_list[i]] = round(sum/sum_divisor, 2)

    return course_assessment_list, lo_assessment_dict

def LOAssessmentView(request, nip, year, semester):
    section = Section.objects.filter(year=year, semester=semester)
    
    if (len(section) == 0):
        return HttpResponseNotFound(f"<h2> Tidak ada course pada semester {semester} - {year}/{int(year)+1}</h2>")
    list_course, lo_assessment = calculateLOAssesment(year, semester)

    ListLOAssessmentPage(request, nip)

    return render(request, 'Dosen/lo_assessment.html', {'lo_assessment':lo_assessment, 'sem':semester, 'tahun1':year, 'tahun2':str(int(year)+1), 'list_matkul':list_course})

def ListLOAssessmentPage(request, nip):
    
    list_tahun_dict = {}
    list_takes = list(Section.objects.all().values())
    for item in list_takes:
        sem = item.get('semester')
        year = item.get('year')
        val = list_tahun_dict.get(year)

        if (val == None):
            list_tahun_dict[year] = []

        list_tahun_dict[year].append(sem)
        list_tahun_dict[year] = list(set(list_tahun_dict.get(year)))
        
    list_tahun = list(list_tahun_dict.keys())

    return render(request, 'Dosen/lo_assessment_list.html', {'nip' : nip, 'list_tahun_dict' : list_tahun_dict, 'list_tahun':list_tahun})

def redirectLOAssessment(request, nip):
    if(request.method == 'POST'):
        semyear = request.POST.get('semyear')
        sem_year_info = semyear.split(', ')
        year = sem_year_info[0]
        semester = sem_year_info[1]

    return redirect('dosen:LOAssessment', nip = nip, year = year, semester = semester)

def countIndeks(year, semester, course_id, section_id):
    
    takes_list = list(Takes.objects.filter(section__course__course_id=course_id, section__semester=semester, section__year = year, section__sec_id = section_id).values('grade'))
    sec_indeks_list = []
    for item in takes_list:
        sec_indeks_list.append(item.get('grade'))
    sec_indeks_list = np.array(sec_indeks_list)
    unique, counts = np.unique(sec_indeks_list, return_counts=True)
    
    return dict(zip(unique, counts))

def TestView(request, nip):
    print(nip)
    return render(request, 'Dosen/test.html', {'nip' : nip})

class TestClassView(generic.ListView):
    template_name = 'Dosen/test.html'
    nip = '14518390'

    def get_queryset(self):
        object_list = self.kwargs['nip']
        return self.kwargs['nip']
