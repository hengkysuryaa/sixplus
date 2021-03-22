from django.contrib import admin
from .models import LO, Course, Section, BobotKomponenScore, Score, Takes, ResponseKerjasama

# Register your models here.
admin.site.register(LO)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Takes)
admin.site.register(BobotKomponenScore)
admin.site.register(Score)
admin.site.register(ResponseKerjasama)
