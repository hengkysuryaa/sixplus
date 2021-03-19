from django.urls import path, re_path
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^FormKerjasama/(?P<course_id>[A-Z0-9]+)/$', views.KerjasamaView, name='FormKerjasama'),
    url(r'^FormKerjasama/(?P<course_id>[A-Z0-9]+)/more/$', views.NextKerjasamaView, name='NextFormKerjasama'),
    url(r'^FormKerjasama/(?P<course_id>[A-Z0-9]+)/Result/', views.SubmitKerjasamaView, name='SubmitFormKerjasama')
]