from django import forms
from .models import Student, DanceClass

# This module defines forms for the Dance Studio application, 
# allowing for the creation and editing of Student and DanceClass models.
# is referenced in html templates to render forms for adding or editing students and dance classes.
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'phone', 'membership_number', 'classes_left']
        widgets = {
            'name': forms.TextInput(attrs={'required': True}),
            'phone': forms.TextInput(attrs={'required': True}),
            'membership_number': forms.TextInput(attrs={'required': True}),
            'classes_left': forms.Select(choices=[(30, '30'), (50, '50'), (100, '100')]),
        }

class DanceClassForm(forms.ModelForm):  # NEW
    class Meta:
        model = DanceClass
        fields = ['name', 'style', 'level', 'description', 'schedule', 'max_students']


'''
The StudentForm is used in the add_student view to handle the creation of new students.
The form is rendered in the add_student.html template, which is designed to display the form fields and handle form submission.
The form is rendered using Django's template system, which allows for dynamic generation of HTML based on the form definition.
The form fields are automatically generated based on the fields defined in the StudentForm class.
This approach ensures that the form is consistent with the model definition and reduces the need for manual HTML coding.

Django Form Rendering in Templates:
    The form is rendered using {{ form.as_p }}, which automatically generates the HTML for all fields defined in the StudentForm.
    This approach ensures that the form fields match the Django form definition without manually specifying them in the template.
Error Handling:
    Validation errors are displayed to the user, both for specific fields and for non-field errors (e.g., general form errors).
Reusability:
    If the StudentForm changes (e.g., a new field is added), the template will automatically reflect those changes without requiring updates to the HTML.'''