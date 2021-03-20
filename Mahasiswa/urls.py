from django.urls import path, re_path
from django.conf.urls import url

from LO.views import KerjasamaView, NextKerjasamaView, SubmitKerjasamaView

urlpatterns = [
    url(r'^FormKerjasama/(?P<course_id>[A-Z0-9]+)/$', KerjasamaView, name='FormKerjasama'),
    url(r'^FormKerjasama/(?P<course_id>[A-Z0-9]+)/more/$', NextKerjasamaView, name='NextFormKerjasama'),
    url(r'^FormKerjasama/(?P<course_id>[A-Z0-9]+)/Result/', SubmitKerjasamaView, name='SubmitFormKerjasama')
]