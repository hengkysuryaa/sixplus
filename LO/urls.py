from django.urls import path

from . import views

urlpatterns = [path('', views.LOView.as_view(), name='index')]