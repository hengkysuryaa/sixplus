from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404

from django.views import generic
from .models import *
from .forms import IdentitasForm, PenilaianKerjasamaForm, IdentitasKomunikasiForm, PenilaianKomunikasiForm, IdentitasKuesionerForm, PenilaianKuesionerForm

from Mahasiswa.models import Student
from User.decorators import allowed_users

import datetime


# KONSTANTA
SEMESTER = 2
YEAR = 2020
SEC_ID = 2

# Create your views here.
# def index(request):
#     return HttpResponse("You're at the LO index")

class LOView(generic.ListView):
    template_name = 'LO/lo_page.html'
    context_object_name = 'lo'
    
    # @allowed_users(['mahasiswa'])
    def get_queryset(self):
        return LO.objects.all().order_by('course_id__course_id')

    # @allowed_users(['mahasiswa'])
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['nip'] = self.kwargs['nip']
        return context

@allowed_users(['mahasiswa'])
def NextKerjasamaView(request, nim, year, semester, course_id, section_id):
    # Check if takes is also valid, if not redirect to home
    takes = Takes.objects.filter(student__nim = nim, section__course__course_id = course_id, section__semester = semester, section__year = year, section__sec_id = section_id)
    if(len(takes) == 0):
        return redirect("mhs:ListFormKerjasama", nim = request.user.first_name)

    identitas = request.user
    kel = request.POST['kelompok']
    penilaian = PenilaianKerjasamaForm()
    return render(request, 'LO/next_form_kerjasama.html', {'nim' : nim, 'identitas':identitas, 'kel':kel, 'penilaian':penilaian,  'year' : year, 'semester' : semester, 'course_id': course_id, 'section_id' : section_id})

@allowed_users(['mahasiswa'])
def KerjasamaView(request, nim, year, semester, course_id, section_id):
    #Checking course_id nya valid gak
    course = get_object_or_404(Course, course_id=course_id)

    # Check if takes is also valid, if not redirect to home
    takes = Takes.objects.filter(student__nim = nim, section__course__course_id = course_id, section__semester = semester, section__year = year, section__sec_id = section_id)
    if(len(takes) == 0):
        return redirect("mhs:ListFormKerjasama", nim = request.user.first_name)

    #identitas = IdentitasForm()
    identitas = request.user
    penilaian = PenilaianKerjasamaForm()

    return render(request, 'LO/form_kerjasama.html', {'nim' : nim, 'penilaian':penilaian, 'year' : year, 'semester' : semester, 'course_id': course_id, 'section_id' : section_id, 'identitas': identitas})

@allowed_users(['mahasiswa'])
def SubmitKerjasamaView(request, nim, year, semester, course_id, section_id):
    # Check if takes is also valid, if not redirect to home
    takes = Takes.objects.filter(student__nim = nim, section__course__course_id = course_id, section__semester = semester, section__year = year, section__sec_id = section_id)
    if(len(takes) == 0):
        return redirect("mhs:ListFormKerjasama", nim = request.user.first_name)

    if (request.POST['NIMPeer'] == request.user.first_name):
        return HttpResponseNotFound("<h2> Tidak bisa menilai diri anda sendiri!</h2> Silakan back ke laman sebelumnya")
    identitas = request.user
    kel = request.POST['kelompok']
    
    student = get_object_or_404(Student, nim=request.POST['NIMPeer'])
    course = get_object_or_404(Course, course_id=course_id)
    #takes = Takes.objects.filter(student = student, section__course__course_id = course_id, section__semester = semester, section__year = year, section__sec_id = section_id)[0]
    res = ResponseKerjasama(takes = takes[0], Kontribusi=int(request.POST['Kontribusi']), PemecahanMasalah=int(request.POST['PemecahanMasalah']), Sikap=int(request.POST['Sikap']), FokusTerhadapTugas=int(request.POST['FokusTerhadapTugas']), BekerjaDenganOrangLain=int(request.POST['BekerjaDenganOrangLain']))
    res.save()

    return render(request, 'LO/form_kerjasama_submit.html', {'nim' : nim, 'identitas':identitas, 'kel':kel,  'year' : year, 'semester' : semester, 'course_id': course_id, 'section_id' : section_id})    

@allowed_users(['mahasiswa'])
def KomunikasiView(request, nim, year, semester, course_id, section_id):
    #Checking course_id nya valid gak
    course = get_object_or_404(Course, course_id=course_id)

    # Check if takes is also valid, if not redirect to home
    takes = Takes.objects.filter(student__nim = nim, section__course__course_id = course_id, section__semester = semester, section__year = year, section__sec_id = section_id)
    if(len(takes) == 0):
        return redirect("mhs:ListFormKomunikasi", nim = request.user.first_name)

    identitas = IdentitasKomunikasiForm()
    penilaian = PenilaianKomunikasiForm()

    return render(request, 'LO/form_komunikasi.html', {'nim' : nim, 'penilaian':penilaian, 'year' : year, 'semester' : semester, 'course_id': course_id, 'section_id' : section_id, 'identitas': identitas})

@allowed_users(['mahasiswa'])
def SubmitKomunikasiView(request, nim, year, semester, course_id, section_id):
    # Check if takes is also valid, if not redirect to home
    takes = Takes.objects.filter(student__nim = nim, section__course__course_id = course_id, section__semester = semester, section__year = year, section__sec_id = section_id)
    if(len(takes) == 0):
        return redirect("mhs:ListFormKomunikasi", nim = request.user.first_name)

    kel = request.POST['kelompok']
    
    student = get_object_or_404(Student, nim=request.POST['NIMPeer'])
    kelompok = request.POST['KelompokPeer']
    course = get_object_or_404(Course, course_id=course_id)
    #takes = Takes.objects.filter(student = student, section__course__course_id = course_id, section__semester = semester, section__year = year, section__sec_id = section_id)[0]
    res = ResponseKomunikasi(takes = takes[0], kelompok = kelompok,  
        Penyampaian1=int(request.POST['Penyampaian1']), Penyampaian2=int(request.POST['Penyampaian2']), Penyampaian3=int(request.POST['Penyampaian3']), Penyampaian4=int(request.POST['Penyampaian4']), 
        Konten=int(request.POST['Konten']), Bahasa=int(request.POST['Bahasa']), Penguasaan=int(request.POST['Penguasaan']), 
        Menjawab=int(request.POST['Menjawab']), Media=int(request.POST['Media']), Waktu=int(request.POST['Waktu'])     
        )
    res.save()

    return render(request, 'LO/form_komunikasi_submit.html', {'nim' : nim, 'kel':kel, 'year' : year, 'semester' : semester, 'course_id': course_id, 'section_id' : section_id})  

@allowed_users(['mahasiswa'])
def NextKomunikasiView(request, nim, year, semester, course_id, section_id):
    # Check if takes is also valid, if not redirect to home
    takes = Takes.objects.filter(student__nim = nim, section__course__course_id = course_id, section__semester = semester, section__year = year, section__sec_id = section_id)
    if(len(takes) == 0):
        return redirect("mhs:ListFormKomunikasi", nim = request.user.first_name)

    kel = request.POST['kelompok']
    penilaian = PenilaianKomunikasiForm()
    return render(request, 'LO/next_form_komunikasi.html', {'nim' : nim,  'kel':kel, 'penilaian':penilaian, 'year' : year, 'semester' : semester, 'course_id': course_id, 'section_id' : section_id})

@allowed_users(['mahasiswa'])
def NextKuesionerView(request, nim, course_id):
    # namaPengisi = request.POST['name']
    # NIMPengisi = request.POST['NIM']
    identitas = request.user
    kel = request.POST['kelompok']
    penilaian = PenilaianKerjasamaForm()
    return render(request, 'LO/next_form_kerjasama.html', {'nim' : nim, 'identitas':identitas, 'kel':kel, 'penilaian':penilaian, 'course_id':course_id})

@allowed_users(['mahasiswa'])
def KuesionerView(request, nim, course_id, year, semester):
    # Get all the takes that semester
    identitas = request.user
    NIM = identitas.first_name
    takes = Takes.objects.filter(student__nim = NIM, section__course__course_id = course_id, section__year = year, section__semester = semester, isKuesionerFilled = False)

    if(len(takes) == 0):
        return redirect("mhs:Home", nim = identitas.first_name)

    penilaian = PenilaianKuesionerForm()

    return render(request, 'LO/form_kuesioner.html', {'nim' : nim, 'penilaian':penilaian, 'course_id': course_id, 'year' : year, 'semester' : semester, 'identitas': identitas})

@allowed_users(['mahasiswa'])
def SubmitKuesionerView(request, nim, course_id, year, semester):
    # namaPengisi = request.POST['name']
    # NIMPengisi = request.POST['NIM']
    identitas = request.user
    NIM = identitas.first_name
    
    #takes = get_object_or_404(Takes, student__nim = NIM, section__course__course_id = course_id, section__year = year, section__semester = semester, isKuesionerFilled = False)
    takes = Takes.objects.filter(student__nim = NIM, section__course__course_id = course_id, section__year = year, section__semester = semester, isKuesionerFilled = False)

    if(len(takes) == 0):
        return redirect("mhs:Home", nim = identitas.first_name)
    res = ResponseKuesioner(takes = takes[0], 
        Kuesioner1=int(request.POST['Kuesioner1']),
        Kuesioner2=int(request.POST['Kuesioner2']),
        Kuesioner3=int(request.POST['Kuesioner3']),
        Kuesioner4=int(request.POST['Kuesioner4']),
        Kuesioner5=int(request.POST['Kuesioner5']),
        Kuesioner6=int(request.POST['Kuesioner6']),
        Kuesioner7=int(request.POST['Kuesioner7']),
        Kuesioner8=int(request.POST['Kuesioner8']),
        Kuesioner9=int(request.POST['Kuesioner9']),
        Kuesioner10=int(request.POST['Kuesioner10']),
        Kuesioner11=int(request.POST['Kuesioner11']),
        Kuesioner12=int(request.POST['Kuesioner12'])
        )
    res.save()
    takes[0].isKuesionerFilled = True
    print(takes)
    takes[0].save()

    return render(request, 'LO/form_kuesioner_submit.html', {'nim' : nim, 'identitas':identitas, 'course_id': course_id, 'year' : year, 'semester' : semester})    

class ListKuesionerView(generic.ListView):
    template_name = 'LO/list_kuesioner.html'
    context_object_name = 'kuesioner_list'

    # @allowed_users(['mahasiswa'])
    def get_queryset(self):
        date = datetime.date.today()
        year = date.year
        month = date.month
        semester = 1

        if(month <= 6):
            year -= 1
            semester = 2
        else:
            semester = 1


        takes = Takes.objects.filter(student__nim = self.kwargs['nim'], section__year = year, section__semester = semester, isKuesionerFilled = False).order_by('section__course__course_id')
        
        return takes

    # @allowed_users(['mahasiswa'])
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        context['nim'] = self.kwargs['nim']
        return context

@allowed_users(['dosen'])
def courseAssessmentPage(request, nip, year, semester):
    section = Section.objects.filter(year=year, semester=semester)
    
    if (len(section) == 0):
        return HttpResponseNotFound(f"<h2> Tidak ada course pada semester {semester} - {year}/{int(year)+1}</h2>")

    refreshCourseAssesmentPage(nip, year, semester)
    courseAssesment_list = CourseAssessmentScore.objects.filter(year = year, semester = semester)

    ##score_list = Score.objects.filter(nim__in = student_list, course = course)

    header = "Semester " + str(semester) + " Tahun " + str(year) + "/" + str(int(year)+1)

    #context = {'dosen' : lecturer}, 'section': sections, 'scores': scores}
    context = {'nip' : nip, 'year' : year, 'semester': semester, 'scores' : courseAssesment_list, 'header' : header}
    return render(request, 'Dosen/course_assessment.html', context)

def refreshCourseAssesmentPage(nip, year, semester):
    section_list = Section.objects.filter(semester = semester, year = year).order_by('course_id', 'sec_id')
    course_list = section_list.values_list('course__course_id', flat = True).distinct()

    for course in course_list:
        course_section_list = section_list.filter(course__course_id = course)
        count = len(course_section_list)
        student_count = 0
        kuesioner_count = 0
        totalKuesioner = 0.0
        totalCourseOutcome = 0.0

        for section in course_section_list:
            takes_list = Takes.objects.filter(section = section)
            section_student = len(takes_list)

            section_courseOutcome = 0.0

            for takes in takes_list:
                if(takes.grade == "A"):
                    section_courseOutcome += 4.0
                elif(takes.grade == "AB"):
                    section_courseOutcome += 3.5
                elif(takes.grade == "B"):
                    section_courseOutcome += 3.0
                elif(takes.grade == "BC"):
                    section_courseOutcome += 2.5
                elif(takes.grade == "C"):
                    section_courseOutcome += 2.0
                elif(takes.grade == "D"):
                    section_courseOutcome += 1.0                
                elif(takes.grade == "T"):
                    section_student -= 1


            responseKuesioner_list = ResponseKuesioner.objects.filter(takes__in = takes_list)
            section_kuesioner = 0.0

            for response in responseKuesioner_list:
                total = response.Kuesioner1 + response.Kuesioner2 + response.Kuesioner3 + response.Kuesioner4 + response.Kuesioner5 + response.Kuesioner6 + response.Kuesioner7 + response.Kuesioner8 + response.Kuesioner9 + response.Kuesioner10 + response.Kuesioner11 + response.Kuesioner12

                total = total / 12

                section_kuesioner += total

            student_count += section_student
            kuesioner_count += len(responseKuesioner_list)
            totalKuesioner += section_kuesioner
            totalCourseOutcome += section_courseOutcome

        if(kuesioner_count== 0):
            totalKuesioner = 0
        else:
            totalKuesioner = round(totalKuesioner/kuesioner_count, 2) 

        if(student_count== 0):
            totalCourseOutcome = 0
        else:
            totalCourseOutcome = round(totalCourseOutcome/student_count, 2)
    
        finalScore = round(((0.5 * totalCourseOutcome) + (0.4 * totalKuesioner) + 0.4) , 2)

        res = CourseAssessmentScore.setCourseAssessment(CourseAssessmentScore, semester = semester, year = year, 
            course_id = course, section_count = count,
            courseOutcomeScore = totalCourseOutcome, kuesionerScore = totalKuesioner, finalScore = finalScore)


@allowed_users(['dosen'])
def ListCourseAssessmentPage(request, nip):
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

    return render(request, 'Dosen/course_assessment_list.html', {'nip' : nip, 'list_tahun_dict' : list_tahun_dict, 'list_tahun':list_tahun})

@allowed_users(['dosen'])
def redirectCourseAssessment(request, nip):
    if(request.method == 'POST'):
        semyear = request.POST.get('semyear')
        sem_year_info = semyear.split(', ')
        year = sem_year_info[0]
        semester = sem_year_info[1]

    return redirect('dosen:CourseAssessment', nip = nip, year = year, semester = semester)
