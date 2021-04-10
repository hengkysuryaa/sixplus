from django.urls import path, re_path
from django.conf.urls import url

from LO.views import KerjasamaView, NextKerjasamaView, SubmitKerjasamaView, KomunikasiView, NextKomunikasiView, SubmitKomunikasiView, ListKuesionerView, KuesionerView, NextKuesionerView, SubmitKuesionerView
from .views import TestView

urlpatterns = [
    url(r'^Suplemen/$', TestView, name='Test'),
    url(r'^FormKerjasama/(?P<course_id>[A-Z0-9]+)/$', KerjasamaView, name='FormKerjasama'),
    url(r'^FormKerjasama/(?P<course_id>[A-Z0-9]+)/more/$', NextKerjasamaView, name='NextFormKerjasama'),
    url(r'^FormKerjasama/(?P<course_id>[A-Z0-9]+)/Result/', SubmitKerjasamaView, name='SubmitFormKerjasama'),
    url(r'^FormKomunikasi/(?P<course_id>[A-Z0-9]+)/$', KomunikasiView, name='FormKomunikasi'),
    url(r'^FormKomunikasi/(?P<course_id>[A-Z0-9]+)/Result/', SubmitKomunikasiView, name='SubmitFormKomunikasi'),
    url(r'^FormKomunikasi/(?P<course_id>[A-Z0-9]+)/more/$', NextKomunikasiView, name='NextFormKomunikasi'),
    url(r'^FormKuesioner/(?P<year>[0-9]+)/(?P<semester>[0-9]+)/$', ListKuesionerView.as_view(), name='ListKuesioner'),
    url(r'^FormKuesioner/(?P<year>[0-9]+)/(?P<semester>[0-9]+)/(?P<course_id>[A-Z0-9]+)/$', KuesionerView, name='FormKuesioner'),
    url(r'^FormKuesioner/(?P<year>[0-9]+)/(?P<semester>[0-9]+)/(?P<course_id>[A-Z0-9]+)/Result/', SubmitKuesionerView, name='SubmitFormKuesioner'),
]