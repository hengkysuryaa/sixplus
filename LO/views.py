from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404

from django.views import generic
from .models import *
from .forms import IdentitasForm, PenilaianKerjasamaForm, IdentitasKomunikasiForm, PenilaianKomunikasiForm, IdentitasKuesionerForm, PenilaianKuesionerForm

from Mahasiswa.models import Student

# KONSTANTA
SEMESTER = 2
YEAR = 2020
SEC_ID = 1

# Create your views here.
# def index(request):
#     return HttpResponse("You're at the LO index")
class LOView(generic.ListView):
    template_name = 'LO/lo_page.html'
    context_object_name = 'lo'

    def get_queryset(self):
        return LO.objects.all().order_by('course_id__course_id')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['nip'] = self.kwargs['nip']
        return context

def NextKerjasamaView(request, nim, course_id):
    # namaPengisi = request.POST['name']
    # NIMPengisi = request.POST['NIM']
    identitas = request.user
    kel = request.POST['kelompok']
    penilaian = PenilaianKerjasamaForm()
    return render(request, 'LO/next_form_kerjasama.html', {'identitas':identitas, 'kel':kel, 'penilaian':penilaian, 'course_id':course_id})

def KerjasamaView(request,nim, course_id):
    #Checking course_id nya valid gak
    course = get_object_or_404(Course, course_id=course_id)
    #TODO: Checking apakah dia takes matkul itu pada semester dan tahun itu(?)

    #identitas = IdentitasForm()
    identitas = request.user
    penilaian = PenilaianKerjasamaForm()

    return render(request, 'LO/form_kerjasama.html', {'penilaian':penilaian, 'course_id': course_id, 'identitas': identitas})

def SubmitKerjasamaView(request,nim, course_id):
    # namaPengisi = request.POST['name']
    # NIMPengisi = request.POST['NIM']
    if (request.POST['NIMPeer'] == request.user.first_name):
        return HttpResponseNotFound("<h2> Tidak bisa menilai diri anda sendiri!</h2> Silakan back ke laman sebelumnya")
    identitas = request.user
    kel = request.POST['kelompok']
    
    student = get_object_or_404(Student, nim=request.POST['NIMPeer'])
    course = get_object_or_404(Course, course_id=course_id)
    takes = Takes.objects.filter(student = student, section__course__course_id = course_id, section__semester = SEMESTER, section__year = YEAR, section__sec_id = SEC_ID)[0]
    res = ResponseKerjasama(takes = takes, Kontribusi=int(request.POST['Kontribusi']), PemecahanMasalah=int(request.POST['PemecahanMasalah']), Sikap=int(request.POST['Sikap']), FokusTerhadapTugas=int(request.POST['FokusTerhadapTugas']), BekerjaDenganOrangLain=int(request.POST['BekerjaDenganOrangLain']))
    res.save()

    return render(request, 'LO/form_kerjasama_submit.html', {'identitas':identitas, 'kel':kel, 'course_id': course_id})    

def KomunikasiView(request, nim, course_id):
    #Checking course_id nya valid gak
    course = get_object_or_404(Course, course_id=course_id)
    #TODO: Checking apakah dia takes matkul itu pada semester dan tahun itu(?)

    identitas = IdentitasKomunikasiForm()
    penilaian = PenilaianKomunikasiForm()

    return render(request, 'LO/form_komunikasi.html', {'nim' : nim, 'penilaian':penilaian, 'course_id': course_id, 'identitas': identitas})

def SubmitKomunikasiView(request, nim, course_id):
    kel = request.POST['kelompok']
    
    student = get_object_or_404(Student, nim=request.POST['NIMPeer'])
    kelompok = request.POST['KelompokPeer']
    course = get_object_or_404(Course, course_id=course_id)
    takes = Takes.objects.filter(student = student, section__course__course_id = course_id, section__semester = SEMESTER, section__year = YEAR, section__sec_id = SEC_ID)[0]
    res = ResponseKomunikasi(takes = takes, kelompok = kelompok,  
        Penyampaian1=int(request.POST['Penyampaian1']), Penyampaian2=int(request.POST['Penyampaian2']), Penyampaian3=int(request.POST['Penyampaian3']), Penyampaian4=int(request.POST['Penyampaian4']), 
        Konten=int(request.POST['Konten']), Bahasa=int(request.POST['Bahasa']), Penguasaan=int(request.POST['Penguasaan']), 
        Menjawab=int(request.POST['Menjawab']), Media=int(request.POST['Media']), Waktu=int(request.POST['Waktu'])     
        )
    res.save()

    return render(request, 'LO/form_komunikasi_submit.html', {'nim' : nim, 'kel':kel, 'course_id': course_id})  

def NextKomunikasiView(request, nim, course_id):
    kel = request.POST['kelompok']
    penilaian = PenilaianKomunikasiForm()
    return render(request, 'LO/next_form_komunikasi.html', {'kel':kel, 'penilaian':penilaian, 'course_id':course_id})

def NextKuesionerView(request, nim, course_id):
    # namaPengisi = request.POST['name']
    # NIMPengisi = request.POST['NIM']
    identitas = request.user
    kel = request.POST['kelompok']
    penilaian = PenilaianKerjasamaForm()
    return render(request, 'LO/next_form_kerjasama.html', {'identitas':identitas, 'kel':kel, 'penilaian':penilaian, 'course_id':course_id})

def KuesionerView(request, nim, course_id, year, semester):
    # Get all the takes that semester
    identitas = request.user
    NIM = identitas.first_name
    takes = get_object_or_404(Takes, student__nim = NIM, section__course__course_id = course_id, section__year = year, section__semester = semester, isKuesionerFilled = False)

    penilaian = PenilaianKuesionerForm()

    return render(request, 'LO/form_kuesioner.html', {'penilaian':penilaian, 'course_id': course_id, 'year' : year, 'semester' : semester, 'identitas': identitas})

def SubmitKuesionerView(request, nim, course_id, year, semester):
    # namaPengisi = request.POST['name']
    # NIMPengisi = request.POST['NIM']
    identitas = request.user
    NIM = identitas.first_name
    
    takes = get_object_or_404(Takes, student__nim = NIM, section__course__course_id = course_id, section__year = year, section__semester = semester, isKuesionerFilled = False)
    res = ResponseKuesioner(takes = takes, 
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
    takes.isKuesionerFilled = True
    takes.save()

    return render(request, 'LO/form_kuesioner_submit.html', {'identitas':identitas, 'course_id': course_id, 'year' : year, 'semester' : semester})    

class ListKuesionerView(generic.ListView):
    template_name = 'LO/list_kuesioner.html'
    context_object_name = 'kuesioner_list'

    def get_queryset(self):
        takes = Takes.objects.filter(student__nim = self.kwargs['nim'], section__year = self.kwargs['year'], section__semester = self.kwargs['semester'], isKuesionerFilled = False).order_by('section__course__course_id')
        
        return takes

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        context['nim'] = self.kwargs['nim']
        context['year'] = self.kwargs['year']
        context['semester'] = self.kwargs['semester']
        return context


def courseAssessmentPage(request, nip, year, semester):
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

            print("Section Outcome", section_courseOutcome)
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
    
        print("Total kuesioner ", totalKuesioner, "count ", count)
        print("Total course outcome ", totalCourseOutcome, "student count ", student_count)
        finalScore = round(((0.5 * totalCourseOutcome) + (0.4 * totalKuesioner) + 0.4) , 2)

        res = CourseAssessmentScore.setCourseAssessment(CourseAssessmentScore, semester = semester, year = year, 
            course_id = course, section_count = count,
            courseOutcomeScore = totalCourseOutcome, kuesionerScore = totalKuesioner, finalScore = finalScore)
