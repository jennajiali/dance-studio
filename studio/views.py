'''
from django.shortcuts import render, redirect
from .models import Student, DanceClass, Attendance
from django.db.models import Q
from datetime import datetime
import csv
from django.http import HttpResponse

def index(request):
    query = request.GET.get('query', '')
    students = Student.objects.filter(
        Q(name__icontains=query) | Q(phone__icontains=query) | Q(membership_number__icontains=query)
    ) if query else Student.objects.all()
    return render(request, 'index.html', {'students': students, 'query': query})

def check_in(request, student_id):
    student = Student.objects.get(id=student_id)
    if student.classes_left > 0:
        student.classes_left -= 1
        student.save()

        now = datetime.now()
        current_hour = now.hour
        current_weekday = now.strftime('%A')

        if current_weekday in ['Monday', 'Wednesday', 'Friday']:
            style = 'Jazz'
        elif current_weekday in ['Tuesday', 'Thursday']:
            style = 'Kpop'
        else:
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

        class_name = f"{level} - {style}"
        dance_class, _ = DanceClass.objects.get_or_create(name=class_name)
        Attendance.objects.create(student=student, dance_class=dance_class)

    return redirect('index')

def add_student(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        membership_number = request.POST['membership_number']
        classes_left = int(request.POST['classes_left'])
        Student.objects.create(
            name=name, phone=phone, membership_number=membership_number, classes_left=classes_left
        )
        return redirect('index')
    return render(request, 'add_student.html')

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
'''

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

@login_required  # NEW: Only allow logged-in staff to access this view for check in
def check_in(request, student_id):
    """Check in a student, decrement their classes left, and log attendance."""
    # Ensure the student exists
    student = get_object_or_404(Student, id=student_id) # TABLE 1

    with transaction.atomic():  # data integrity ensured
        '''Either all the operations succeed, or none of them are applied to the database.
        i.e. Ensures that all database operations within its block are executed as a single atomic transaction. 

        If any operation inside this block fails (e.g., saving the student or creating an Attendance record), all changes made within the block are rolled back.
        This ensures that the student's classes_left is not decremented if the attendance record cannot be created, maintaining data integrity.
        '''

        # Refresh the student instance to get the latest data
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
            '''A Django ORM (Object-Relational Mapping) query.
            DanceClass is a Django model representing a database table.
                .objects is the manager that allows you to query the database.
                .filter(style=style, level=level) retrieves all records from the DanceClass table 
                where the style column matches the style variable and the level column matches the level variable.
            The result is a QuerySet, which is a collection of matching records.
            
            .first() returns the first record from the QuerySet or None if no records match.
            This is useful for checking if a class exists for the given style and level.
            If no class is found, we create a new one.'''
            dance_class = DanceClass.objects.filter(style=style, level=level).first()
            if not dance_class: 
                # Fallback: create (or get) by class name, along with style and level
                class_name = f"{level} - {style}"

                '''A Django ORM method that either retrieves an existing record or creates a new one if it doesn't exist.

                Parameters:
                    name=class_name: The name of the dance class (e.g., "Basic - Jazz").
                    defaults={...}: A dictionary of default values to use if a new DanceClass is created.
                
                Defaults Provided:
                    "style": style: The style of the dance (e.g., "Jazz").
                    "level": level: The level of the class (e.g., "Basic").
                    "description": f"{level} {style} class": A description of the class (e.g., "Basic Jazz class").
                    "schedule": f"{current_weekday} {current_hour}:00": The schedule of the class (e.g., "Monday 17:00").
                    "max_students": 20: The maximum number of students allowed in the class.
                Return Values:
                - dance_class: The retrieved or newly created DanceClass object.
                - created: A boolean indicating whether a new object was created (True) or an existing one was retrieved (False).'''
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
                pass  # Prevent duplicate check-in for same class/date
            ### If a duplicate attendance record (for same class/date) is attempted, it is silently ignored to prevent errors. 

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

# allows the manager to check per-student attendance history
@login_required
def student_attendance_history(request, student_id):
    """Display the attendance history for a specific student."""
    # Ensure the student exists, or return a 404 error if not found
    student = get_object_or_404(Student, id=student_id)

    # Fetch attendance records for the student, ordered by date and time
    # Using select_related to optimize database queries by fetching related DanceClass objects in a single query
    attendance_records = Attendance.objects.filter(student=student).select_related('dance_class').order_by('-date', '-time')
    
    # Render the attendance history template with the student and their attendance records
    return render(request, 'student_attendance_history.html', {
        'student': student,
        'attendance_records': attendance_records
    })