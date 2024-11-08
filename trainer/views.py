from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.apps import apps
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Trainer

def homepage_trainer(request):
    return render(request, 'trainer/trainer_homepage.html')


def assigned_courses(request):
    course = apps.get_model('admin_app', 'Course')
    trainer = request.user
    courses = course.objects.filter(trainer=trainer)
    return render(request, 'trainer/assigned_courses.html', {'courses': courses})


@login_required
def course_detail(request, course_id):
    course = apps.get_model('admin_app', 'Course')
    # Fetch the course based on the course_id and ensure the logged-in user is the assigned trainer
    course = get_object_or_404(course, id=course_id, trainer=request.user)

    # Render the course detail template with the course context
    return render(request, 'trainer/course_info.html', {'course': course})


from django.shortcuts import render
from django.apps import apps

def trainer_assigned_employees(request):
    # Dynamically load the Course and EmployeeCourse models
    Course = apps.get_model('admin_app', 'Course')
    EmployeeCourse = apps.get_model('employee', 'EmployeeCourse')  # Replace 'employee' with the correct app name

    # Get the logged-in trainer (assuming the logged-in user is a trainer)
    trainer = request.user

    # Fetch the courses where this trainer is assigned
    courses = Course.objects.filter(trainer=trainer)

    # Create an empty list to collect assigned employees
    employees = []

    # Loop through each course to find employees assigned to each course
    for course in courses:
        # Get EmployeeCourse instances for each course
        employee_courses = EmployeeCourse.objects.filter(course=course)

        # Extract the employees from these instances and add them to the list
        for ec in employee_courses:
            employees.append(ec.employee)

    # Pass the list of employees to the context
    context = {
        'employees': employees
    }

    return render(request, 'trainer/assigned_employees.html', context)


from django.shortcuts import render, get_object_or_404
from django.apps import apps


def trainer_courses(request, trainer_id):
    # Dynamically get the Trainer, EmployeeCourse, and Course models from their respective apps

    EmployeeCourse = apps.get_model('employee','EmployeeCourse')
    Course = apps.get_model('admin_app', 'Course')  # Assuming 'Course' model is in 'admin_app'

    # Get the trainer object
    trainer = get_object_or_404(Trainer, id=trainer_id)

    # Get all the courses assigned to this trainer
    assigned_courses = trainer.assigned_courses.all()

    # Dictionary to store employees by course
    employees_by_course = {}

    for course in assigned_courses:
        # Get all EmployeeCourse instances for this course (no select_related needed)
        employee_courses = EmployeeCourse.objects.filter(course=course)

        # Extract the employees from the EmployeeCourse instances
        employees = [ec.employee for ec in employee_courses]

        # Add the course and its employees to the dictionary
        employees_by_course[course] = employees

    context = {
        'trainer': trainer,
        'employees_by_course': employees_by_course,
    }

    return render(request, 'trainer/trainer_courses.html', context)


