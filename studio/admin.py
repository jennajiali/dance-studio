# Register your models with the Django admin site
from django.contrib import admin
from .models import Student, DanceClass, Attendance

@admin.register(Student) 
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'membership_number', 'classes_left')

@admin.register(DanceClass) 
class DanceClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'style', 'level', 'schedule', 'max_students')

@admin.register(Attendance) 
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'dance_class', 'date', 'time')