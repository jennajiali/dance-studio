from django.db import models

'''
This module defines the models (design of the database structure) for the dance studio application.
It includes models for DanceClass, Student, and Attendance, which represent the dance classes offered and the students information, connected via their attendance records.
DanceClass table represents a dance class with fields for name, description, schedule, and maximum number of students.
Student table represents a student with fields for name, phone number, membership number, and the number of classes left in their membership.
Attendance table represents the attendance of a student in a dance class, including the student, class, date, and time of attendance.

many-to-many relationship between DanceClass and Student is established via Attendance,
foreign keys are used to link Attendance to both Student and DanceClass models.
This structure allows for efficient management of dance classes, students, and their attendance records.
'''

'''

class DanceClass(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    schedule = models.CharField(max_length=200)  # e.g., "Mon 6-7 PM, Wed 6-7 PM"
    max_students = models.PositiveIntegerField(default=20)

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    membership_number = models.CharField(max_length=20, unique=True)
    classes_left = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.membership_number})"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    dance_class = models.ForeignKey(DanceClass, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.dance_class.name} on {self.date} at {self.time}"
'''


class DanceClass(models.Model):
    '''This model represents a dance class with fields for name, style, level, description, schedule, and maximum number of students.'''
    # Define choices for style and level
    STYLE_CHOICES = [
        ('Jazz', 'Jazz'),
        ('Kpop', 'Kpop'),
        ('Hip-hop', 'Hip-hop'),
        ('House', 'House'),
        ('Urban', 'Urban'),
    ]
    LEVEL_CHOICES = [
        ('Basic', 'Basic'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Unknown', 'Unknown'),
    ]
    # Fields for the DanceClass model
    name = models.CharField(max_length=100)
    style = models.CharField(max_length=20, choices=STYLE_CHOICES, default='Jazz')  # NEW
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='Basic') # NEW
    description = models.TextField(blank=True, null=True, default="")
    schedule = models.CharField(max_length=200, blank=True, null=True, default="")
    max_students = models.PositiveIntegerField(default=20)

    def __str__(self):
        '''Returns a string representation of the dance class, including its name, level, and style.'''
        return f"{self.name} ({self.level} - {self.style})"

class Student(models.Model):
    '''This model represents a student with fields for name, phone number, membership number, and the number of classes left in their membership.'''
    # Fields for the Student model
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    membership_number = models.CharField(max_length=20, unique=True)
    classes_left = models.PositiveIntegerField(default=0)

    def __str__(self):
        '''Returns a string representation of the student, including their name and membership number.'''
        return f"{self.name} ({self.membership_number})"

class Attendance(models.Model):
    '''This model represents the attendance of a student in a dance class, including the student, class, date, and time of attendance.'''
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    dance_class = models.ForeignKey(DanceClass, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    class Meta:
        '''Meta class to define unique constraints for the Attendance model.'''
        # Ensure that a student can only have one attendance record for a specific dance class on a specific date, duplicates are not allowed.
        # This prevents multiple attendance records for the same student in the same class on the same date.
        # This is useful for tracking attendance accurately.
        # It ensures that each attendance record is unique for a student, dance class, and date combination.
        # This is useful for preventing duplicate attendance records.
        unique_together = ('student', 'dance_class', 'date')

    def __str__(self):
        '''Returns a string representation of the attendance record, including the student's name, dance class name, date, and time.'''
        return f"{self.student.name} - {self.dance_class.name} on {self.date} at {self.time}"