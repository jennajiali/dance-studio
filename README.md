# Dance Studio Management System

A Django-based web application for managing a dance studio, including student registrations, class check-ins, attendance tracking, and more.

## Features
- **Student Management**: Add, edit, and manage student details.
- **Class Management**: Add and manage dance classes with styles, levels, and schedules.
- **Attendance Tracking**: Log and view attendance records for students.
- **Export Attendance**: Download attendance records as a CSV file.
- **Authentication**: Secure login/logout for staff members.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/dance-studio.git
   cd dance-studio

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
    

3. Set up the database:
   ```bash
    python manage.py migrate
4. Create a superuser for admin access:
   ```bash
   python manage.py createsuperuser

6. Run the development server
   ```bash
   python manage.py runserver
   
7. Open the application in your browser: http://127.0.0.1:8000/

## Usage
- Log in with the superuser account to access admin features.
- Add students and dance classes via the UI.
- Check in students and track attendance.
