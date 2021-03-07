from django.urls import path
from User.views import *

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('register/', registerPage, name='register'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
    
]