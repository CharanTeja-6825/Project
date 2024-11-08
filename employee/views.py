from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import ProfileForm, UpdatePasswordForm
from django.apps import apps
from .models import EmployeeCourse

def homepage_employee(request):
    return render(request, 'employee/employee_homepage.html')

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('employee:profile_page')
    else:
        form = ProfileForm(instance=request.user)
        messages.error(request, 'An error occurred While performing the Action')

    return render(request, 'employee/employee_profile.html', {'form': form})


def update_password(request):
    if request.method == 'POST':
        form = UpdatePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('employee:profile_page')
        else:
            print(form.errors)  # For debugging
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UpdatePasswordForm(user=request.user)

    return render(request, 'employee/employee_profile.html', {'password_form': form})

@login_required
def profile_page(request):
    return render(request, 'employee/employee_profile.html', {
        'user': request.user,
    })

@login_required
def course_list(request):
    Course = apps.get_model('admin_app', 'Course')
    courses = Course.objects.all()
    print(courses)  # Add this line to see what courses are retrieved
    return render(request, 'employee/assigned_courses.html', {'courses': courses})

@login_required
def course_detail(request, course_id):  # Ensure this accepts course_id
    Course = apps.get_model('admin_app', 'Course')
    course = get_object_or_404(Course, id=course_id)  # Fetch the specific course by ID
    return render(request, 'employee/course_details.html', {'course': course})


@login_required
def add_course_to_employee(request):
    Course = apps.get_model('admin_app', 'Course')
    courses = Course.objects.all()  # Fetch all available courses

    if request.method == 'POST':
        course_id = request.POST.get('course')
        employee = request.user  # Assuming employee is the logged-in user

        # Fetch the selected course
        course = get_object_or_404(Course, id=course_id)

        # Create or add the course to the EmployeeCourse model
        EmployeeCourse.objects.create(employee=employee, course=course)

        # Redirect to some success or management page
        return redirect('employee:homepage_employee')  # Replace with your desired redirect URL

    return render(request, 'employee/add_course.html', {'courses': courses})