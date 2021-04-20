from django.urls import path, re_path
from django.conf.urls import url
from Dosen.views import penilaianPage, showPenilaianPage

from . import views
from LO.views import LOView, courseAssessmentPage
from User.views import logoutUser

urlpatterns = [
    		url(r'^logout/$', logoutUser, name='logout'),
			url(r'^OMM/$', LOView.as_view(), name='OMM'),
			url(r'^Test/$', views.TestClassView.as_view(), name='test'),
			re_path(r'^Nilai/$', showPenilaianPage, name='SectionWithTeaches'),
			re_path(r'^Nilai/GetSection2$', views.SectionPage2, name='GetSection2'),
			re_path(r'^Nilai/(?P<year>[0-9]+)/(?P<semester>[0-9]+)/$', views.DosenSectionListView.as_view(), name='SectionList'),
			re_path(r'^Nilai/(?P<year>[0-9]+)/(?P<semester>[0-9]+)/GetSection$', views.SectionPage, name='GetSection'),
			re_path(r'^Nilai/(?P<year>[0-9]+)/(?P<semester>[0-9]+)/(?P<course_id>[A-Z0-9]+)/(?P<section_id>[0-9]+)/$', penilaianPage, name='SectionPage'),
			re_path(r'^Nilai/(?P<year>[0-9]+)/(?P<semester>[0-9]+)/(?P<course_id>[A-Z0-9]+)/(?P<section_id>[0-9]+)/Upload/$', views.importListMhs, name='ExcelUpload'),
			re_path(r'^Nilai/(?P<year>[0-9]+)/(?P<semester>[0-9]+)/(?P<course_id>[A-Z0-9]+)/(?P<section_id>[0-9]+)/Download/$', views.exportListMhs, name='ExcelDownload'),
			re_path(r'^Nilai/(?P<year>[0-9]+)/(?P<semester>[0-9]+)/(?P<course_id>[A-Z0-9]+)/(?P<section_id>[0-9]+)/SetIndeks/$', views.BobotIndeksView, name='BobotIndeks'),
			re_path(r'^Nilai/(?P<year>[0-9]+)/(?P<semester>[0-9]+)/(?P<course_id>[A-Z0-9]+)/(?P<section_id>[0-9]+)/SetIndeks/Submit/$', views.BobotIndeksSubmitView, name='BobotIndeksSubmit'),
            url(r'^KomponenNilai/$', views.DistribusiKomponenNilaiView.as_view(), name='KomponenNilai'),
            url(r'^KomponenNilai/(?P<course_id>[A-Z0-9]+)/$', views.FormsDistribusiNilai, name='FormKomponen'),
            url(r'^KomponenNilai/(?P<course_id>[A-Z0-9]+)/Result/$', views.SubmitView, name='Submit'),
            path('penilaian', penilaianPage, name = 'penilaian'),
			re_path(r'^CourseAssessment/(?P<year>[0-9]+)/(?P<semester>[0-9]+)/$', courseAssessmentPage, name='CourseAssessment'),
			re_path(r'^LOAssessment/(?P<year>[0-9]+)/(?P<semester>[0-9]+)/$', views.LOAssessmentView, name='LOAssessment'),
			re_path(r'^LOAssessment/$', views.ListLOAssessmentPage, name='LOAssessmentList'),
			re_path(r'^LOAssessment/Submit/$', views.redirectLOAssessment, name='SubmitLOAssessmentList'),
			url(r'', views.HomepageDosenView, name='Home'),
]
