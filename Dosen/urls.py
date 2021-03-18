from django.urls import path
from django.conf.urls import url

from . import views
from LO.views import LOView

urlpatterns = [url(r'^OMM/$', LOView.as_view(), name='OMM'),
            url(r'^KomponenNilai/$', views.DistribusiKomponenNilaiView.as_view(), name='KomponenNilai'),
            url(r'^KomponenNilai/(?P<course_id>[A-Z0-9]+)/$', views.FormsDistribusiNilai, name='FormKomponen'),
            url(r'^KomponenNilai/(?P<course_id>[A-Z0-9]+)/Result/$', views.SubmitView, name='Submit'),
            url(r'^KomponenNilai/(?P<course_id>[A-Z0-9]+)/Export/$', views.exportListMhs, name='Export'),
            url(r'^KomponenNilai/(?P<course_id>[A-Z0-9]+)/Import/$', views.FormsImportNilai, name='FormImport'),
            url(r'^KomponenNilai/(?P<course_id>[A-Z0-9]+)/Import/Berhasil/$', views.importListMhs, name='Import')

]