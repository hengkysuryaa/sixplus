from django.urls import path, re_path
from django.conf.urls import url
from . import views

from LO.views import *
from .views import TestView, LOSuplemenSemesterView
from User.views import logoutUser
from User.decorators import allowed_users


urlpatterns = [
    url(r'^logout/$', logoutUser, name='logout'),
    url(r'^Suplemen/$', TestView, name='Test'),
    url(r'^LOSuplemen/$', LOSuplemenSemesterView, name='ViewLOSuplemen'),
    re_path(r'^FormKerjasama/(?P<year>[0-9]+)/(?P<semester>[0-9]+)/(?P<course_id>[A-Z0-9]+)/(?P<section_id>[0-9]+)/$', KerjasamaView, name='FormKerjasama'),
    re_path(r'^FormKerjasama/(?P<year>[0-9]+)/(?P<semester>[0-9]+)/(?P<course_id>[A-Z0-9]+)/(?P<section_id>[0-9]+)/more/$', NextKerjasamaView, name='NextFormKerjasama'),
    re_path(r'^FormKerjasama/(?P<year>[0-9]+)/(?P<semester>[0-9]+)/(?P<course_id>[A-Z0-9]+)/(?P<section_id>[0-9]+)/Result/', SubmitKerjasamaView, name='SubmitFormKerjasama'),
    re_path(r'^FormKomunikasi/(?P<year>[0-9]+)/(?P<semester>[0-9]+)/(?P<course_id>[A-Z0-9]+)/(?P<section_id>[0-9]+)/$', KomunikasiView, name='FormKomunikasi'),
    re_path(r'^FormKomunikasi/(?P<year>[0-9]+)/(?P<semester>[0-9]+)/(?P<course_id>[A-Z0-9]+)/(?P<section_id>[0-9]+)/Result/', SubmitKomunikasiView, name='SubmitFormKomunikasi'),
    re_path(r'^FormKomunikasi/(?P<year>[0-9]+)/(?P<semester>[0-9]+)/(?P<course_id>[A-Z0-9]+)/(?P<section_id>[0-9]+)/more/$', NextKomunikasiView, name='NextFormKomunikasi'),
    re_path(r'^FormKuesioner/(?P<year>[0-9]+)/(?P<semester>[0-9]+)/$', allowed_users(['mahasiswa'])(ListKuesionerView.as_view()), name='ListKuesioner'),
    re_path(r'^FormKuesioner/(?P<year>[0-9]+)/(?P<semester>[0-9]+)/(?P<course_id>[A-Z0-9]+)/$', KuesionerView, name='FormKuesioner'),
    re_path(r'^FormKuesioner/(?P<year>[0-9]+)/(?P<semester>[0-9]+)/(?P<course_id>[A-Z0-9]+)/Result/', SubmitKuesionerView, name='SubmitFormKuesioner'),
    url(r'', views.HomepageMahasiswaView, name='Home'),
]