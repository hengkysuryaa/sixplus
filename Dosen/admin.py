from django.contrib import admin
from .models import Lecturer, Teaches, BobotIndeks

# Register your models here.
admin.site.register(Lecturer)
admin.site.register(Teaches)
admin.site.register(BobotIndeks)