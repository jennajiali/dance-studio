from django.urls import path
from . import views  # Import views from the current directory

urlpatterns = [
    # Define URL patterns for the studio app, mapping URLs to their corresponding views.
    path('', views.index, name='index'),
    path('check_in/<int:student_id>/', views.check_in, name='check_in'),
    path('add_student/', views.add_student, name='add_student'),
    path('add_dance_class/', views.add_dance_class, name='add_dance_class'), 
    path('export_attendance_csv/', views.export_attendance_csv, name='export_attendance_csv'),
    path('student/<int:student_id>/attendance/', views.student_attendance_history, name='student_attendance_history'),  # NEW
]

# It includes paths for the index page, checking in students, adding new students, and exporting attendance data as CSV.
# This allows the studio app to handle its own URL routing, keeping the project modular and organized.


