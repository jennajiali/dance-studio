from django.db import models
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
        '''Meta class to define unique constraints for the Attendance model.''' c
        unique_together = ('student', 'dance_class', 'date')

    def __str__(self):
        '''Returns a string representation of the attendance record, including the student's name, dance class name, date, and time.'''
        return f"{self.student.name} - {self.dance_class.name} on {self.date} at {self.time}"