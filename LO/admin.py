from django.contrib import admin
from .models import LO, Course, Section, Takes

# Register your models here.
admin.site.register(LO)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Takes)