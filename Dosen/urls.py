from django.urls import path
from django.conf.urls import url
from Dosen.views import penilaianPage

from . import views

urlpatterns = [url(r'^KomponenNilai/$', views.DistribusiKomponenNilaiView.as_view(), name='KomponenNilai'),
            url(r'^KomponenNilai/(?P<course_id>[A-Z0-9]+)/$', views.FormsDistribusiNilai, name='FormKomponen'),
            url(r'^KomponenNilai/(?P<course_id>[A-Z0-9]+)/Result/$', views.SubmitView, name='Submit'),
            path('penilaian', penilaianPage, name = 'penilaian'),
]
