from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404

from django.views import generic
from .models import LO, Course, ResponseKerjasama, ResponseKomunikasi, Takes
from .forms import IdentitasForm, PenilaianKerjasamaForm, IdentitasKomunikasiForm, PenilaianKomunikasiForm

from Mahasiswa.models import Student

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

def NextKerjasamaView(request, course_id):
    # namaPengisi = request.POST['name']
    # NIMPengisi = request.POST['NIM']
    identitas = request.user
    kel = request.POST['kelompok']
    penilaian = PenilaianKerjasamaForm()
    return render(request, 'LO/next_form_kerjasama.html', {'identitas':identitas, 'kel':kel, 'penilaian':penilaian, 'course_id':course_id})

def KerjasamaView(request, course_id):
    #Checking course_id nya valid gak
    course = get_object_or_404(Course, course_id=course_id)
    #TODO: Checking apakah dia takes matkul itu pada semester dan tahun itu(?)

    #identitas = IdentitasForm()
    identitas = request.user
    penilaian = PenilaianKerjasamaForm()

    return render(request, 'LO/form_kerjasama.html', {'penilaian':penilaian, 'course_id': course_id, 'identitas': identitas})

def SubmitKerjasamaView(request, course_id):
    # namaPengisi = request.POST['name']
    # NIMPengisi = request.POST['NIM']
    if (request.POST['NIMPeer'] == request.user.first_name):
        return HttpResponseNotFound("<h2> Tidak bisa menilai diri anda sendiri!</h2> Silakan back ke laman sebelumnya")
    identitas = request.user
    kel = request.POST['kelompok']
    
    student = get_object_or_404(Student, nim=request.POST['NIMPeer'])
    course = get_object_or_404(Course, course_id=course_id)
    takes = Takes.objects.filter(student = student, section__course__course_id = course_id, section__semester = 1, section__year = 2020, section__sec_id = 1)[0]
    res = ResponseKerjasama(takes = takes, Kontribusi=int(request.POST['Kontribusi']), PemecahanMasalah=int(request.POST['PemecahanMasalah']), Sikap=int(request.POST['Sikap']), FokusTerhadapTugas=int(request.POST['FokusTerhadapTugas']), BekerjaDenganOrangLain=int(request.POST['BekerjaDenganOrangLain']))
    res.save()

    return render(request, 'LO/form_kerjasama_submit.html', {'identitas':identitas, 'kel':kel, 'course_id': course_id})    

def KomunikasiView(request, course_id):
    #Checking course_id nya valid gak
    course = get_object_or_404(Course, course_id=course_id)
    #TODO: Checking apakah dia takes matkul itu pada semester dan tahun itu(?)

    identitas = IdentitasKomunikasiForm()
    penilaian = PenilaianKomunikasiForm()

    return render(request, 'LO/form_komunikasi.html', {'penilaian':penilaian, 'course_id': course_id, 'identitas': identitas})

def SubmitKomunikasiView(request, course_id):
    kel = request.POST['kelompok']
    
    student = get_object_or_404(Student, nim=request.POST['NIMPeer'])
    kelompok = request.POST['KelompokPeer']
    course = get_object_or_404(Course, course_id=course_id)
    takes = Takes.objects.filter(student = student, section__course__course_id = course_id, section__semester = 1, section__year = 2020, section__sec_id = 1)[0]
    res = ResponseKomunikasi(takes = takes, kelompok = kelompok,  
        Penyampaian1=int(request.POST['Penyampaian1']), Penyampaian2=int(request.POST['Penyampaian2']), Penyampaian3=int(request.POST['Penyampaian3']), Penyampaian4=int(request.POST['Penyampaian4']), 
        Konten=int(request.POST['Konten']), Bahasa=int(request.POST['Bahasa']), Penguasaan=int(request.POST['Penguasaan']), 
        Menjawab=int(request.POST['Menjawab']), Media=int(request.POST['Media']), Waktu=int(request.POST['Waktu'])     
        )
    res.save()

    return render(request, 'LO/form_komunikasi_submit.html', {'kel':kel, 'course_id': course_id})  

def NextKomunikasiView(request, course_id):
    kel = request.POST['kelompok']
    penilaian = PenilaianKomunikasiForm()
    return render(request, 'LO/next_form_komunikasi.html', {'kel':kel, 'penilaian':penilaian, 'course_id':course_id})