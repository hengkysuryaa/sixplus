from django.shortcuts import render
from django.http import HttpResponse

from django.views import generic
from .models import LO

# Create your views here.
# def index(request):
#     return HttpResponse("You're at the LO index")
class LOView(generic.ListView):
    template_name = 'LO/lo_page.html'
    context_object_name = 'lo'

    def get_queryset(self):
        return LO.objects.all().order_by('course_id')
