from django import forms
from .models import Student, DanceClass

# This module defines forms for the Dance Studio application, 
# allowing for the creation and editing of Student and DanceClass models.
# is referenced in html templates to render forms for adding or editing students and dance classes.

class StudentForm(forms.ModelForm):
    """
    Form for creating or updating a Student instance.
    This form includes fields for the student's name, phone number, membership number,
    and the number of classes left in their membership.
    """
    class Meta:
        model = Student
        fields = ['name', 'phone', 'membership_number', 'classes_left']
        widgets = {
            'name': forms.TextInput(attrs={'required': True}),
            'phone': forms.TextInput(attrs={'required': True}),
            'membership_number': forms.TextInput(attrs={'required': True}),
            'classes_left': forms.Select(choices=[(30, '30'), (50, '50'), (100, '100')]),
        }

class DanceClassForm(forms.ModelForm):  
    """
    Form for creating or updating a DanceClass instance.
    This form includes fields for the class name, style, level, description, schedule,
    and maximum number of students allowed in the class.
    """
    class Meta:
        model = DanceClass
        fields = ['name', 'style', 'level', 'description', 'schedule', 'max_students']


