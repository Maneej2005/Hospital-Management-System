from django.contrib import admin

# Register your models here.

from . models import Student,college

admin.site.register(Student)
admin.site.register(college)