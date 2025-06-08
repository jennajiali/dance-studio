from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, DanceClass, Attendance
from .forms import StudentForm, DanceClassForm
from django.db.models import Q
from django.db import IntegrityError, transaction
from datetime import datetime
import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required  # NEW

def index(request):
    """Display the index page with a list of students and a search query."""
    query = request.GET.get('query', '')
    students = Student.objects.filter(
        Q(name__icontains=query) | Q(phone__icontains=query) | Q(membership_number__icontains=query)
    ) if query else Student.objects.all()
    return render(request, 'index.html', {'students': students, 'query': query})

@login_required
def check_in(request, student_id):
    """Check in a student, decrement their classes left, and log attendance."""
    # Ensure the student exists
    student = get_object_or_404(Student, id=student_id)  # TABLE 1: Fetching student by ID

    with transaction.atomic():  # context manager ensures data integrity before committing changes
        student.refresh_from_db()
        if student.classes_left > 0:
            student.classes_left -= 1
            student.save()

            now = datetime.now() 
            current_hour = now.hour
            current_weekday = now.strftime('%A')  # Get the current weekday

            # Try to find a scheduled class for this time/weekday
            weekday_map = {
                'Monday': 'Jazz',
                'Wednesday': 'Jazz',
                'Friday': 'Jazz',
                'Tuesday': 'Kpop',
                'Thursday': 'Kpop'}
            style = weekday_map.get(current_weekday)  # Default style based on weekday using a dictionary
            if not style: # If not found, determine style based on hour
                if current_hour == 17:
                    style = 'Hip-hop'
                elif current_hour == 18:
                    style = 'House'
                else:
                    style = 'Urban'

            if current_hour == 17:
                level = 'Basic'
            elif current_hour == 18:
                level = 'Intermediate'
            elif current_hour == 19:
                level = 'Advanced'
            else:
                level = 'Unknown'

            # TABLE 2: finding or creating a dance class
            # Try to find a scheduled class from DB using only style and level
            dance_class = DanceClass.objects.filter(style=style, level=level).first()
            if not dance_class: 
                # Fallback: create (or get) by class name, along with style and level
                class_name = f"{level} - {style}"

                dance_class, created = DanceClass.objects.get_or_create(
                    name=class_name,
                    defaults={
                        "style": style,
                        "level": level,
                        "description": f"{level} {style} class",
                        "schedule": f"{current_weekday} {current_hour}:00",
                        "max_students": 20,
                    }
                )

            # TABLE 3: logging attendance
            # Creates a new Attendance record to log the student's check-in for the class.
            try:
                Attendance.objects.create(student=student, dance_class=dance_class)
            except IntegrityError:
                pass  # Silently ignore duplicate check-in for same class/date

    # Redirect to the index page after check-in process is complete
    return redirect('index') 

@login_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('index')
            except IntegrityError:
                form.add_error(None, "Phone or Membership number already exists.")
    else:
        form = StudentForm()
    return render(request, 'add_student.html', {'form': form})

@login_required
def add_dance_class(request):  # NEW: UI for staff to add classes
    if request.method == 'POST':
        form = DanceClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = DanceClassForm()
    return render(request, 'add_dance_class.html', {'form': form})

@login_required
def export_attendance_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance.csv"'

    writer = csv.writer(response)
    writer.writerow(['Student Name', 'Membership Number', 'Class Name', 'Date', 'Time'])

    for record in Attendance.objects.select_related('student', 'dance_class').all():
        writer.writerow([
            record.student.name,
            record.student.membership_number,
            record.dance_class.name,
            record.date,
            record.time
        ])

    return response

@login_required
def student_attendance_history(request, student_id):
    """Display the attendance history for a specific student."""
    student = get_object_or_404(Student, id=student_id)

    # Fetch attendance records for the student, ordered by date and time in descending order (most recent first, hence the dash sign)
    attendance_records = Attendance.objects.filter(student=student).select_related('dance_class').order_by('-date', '-time') 
    
    # Render the attendance history template with the student and their attendance records
    return render(request, 'student_attendance_history.html', {
        'student': student,
        'attendance_records': attendance_records
    })