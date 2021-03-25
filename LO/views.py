from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from django.views import generic
from .models import LO, Course, ResponseKerjasama
from .forms import IdentitasForm, PenilaianKerjasamaForm

from Mahasiswa.models import Student

# Create your views here.
# def index(request):
#     return HttpResponse("You're at the LO index")
class LOView(generic.ListView):
    template_name = 'LO/lo_page.html'
    context_object_name = 'lo'

    def get_queryset(self):
        return LO.objects.all().order_by('course_id__course_id')

def NextKerjasamaView(request, course_id):
    namaPengisi = request.POST['name']
    NIMPengisi = request.POST['NIM']
    kel = request.POST['kelompok']
    penilaian = PenilaianKerjasamaForm()
    return render(request, 'LO/next_form_kerjasama.html', {'nama':namaPengisi, 'nim':NIMPengisi, 'kel':kel, 'penilaian':penilaian, 'course_id':course_id})

def KerjasamaView(request, course_id):
    #Checking course_id nya valid gak
    course = get_object_or_404(Course, course_id=course_id)
    #TODO: Checking apakah dia takes matkul itu pada semester dan tahun itu(?)

    identitas = IdentitasForm()
    penilaian = PenilaianKerjasamaForm()

    return render(request, 'LO/form_kerjasama.html', {'penilaian':penilaian, 'course_id': course_id, 'identitas': identitas})

def SubmitKerjasamaView(request, course_id):
    namaPengisi = request.POST['name']
    NIMPengisi = request.POST['NIM']
    kel = request.POST['kelompok']
    
    student = get_object_or_404(Student, nim=request.POST['NIMPeer'])
    course = get_object_or_404(Course, course_id=course_id)
    res = ResponseKerjasama(student=student, course=course, Kontribusi=int(request.POST['Kontribusi']), PemecahanMasalah=int(request.POST['PemecahanMasalah']), Sikap=int(request.POST['Sikap']), FokusTerhadapTugas=int(request.POST['FokusTerhadapTugas']), BekerjaDenganOrangLain=int(request.POST['BekerjaDenganOrangLain']))
    res.save()

    return render(request, 'LO/form_kerjasama_submit.html', {'nama':namaPengisi, 'nim':NIMPengisi, 'kel':kel, 'course_id': course_id})    

