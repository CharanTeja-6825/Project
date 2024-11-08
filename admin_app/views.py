from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth import logout
from django.db.models.functions import Length
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Course  # Assuming Course is your model for courses
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .forms import UpdatePasswordForm, CourseForm


def homepage(request):
    return render(request, 'admin_app/project_homepage.html')


def register(request):
    if request.method == 'POST':
        # Get form data
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Validate passwords
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('admin_app:register')  # Replace 'register' with your registration page URL name

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('admin_app:register')

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('admin_app:register')

        # Create a new user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = firstname
        user.last_name = lastname
        user.save()

        messages.success(request, 'Registration successful. You can now log in.')
        return redirect('admin_app:user_login')  # Replace 'user_login' with your login page URL name

    return render(request, 'admin_app/register.html')  # Replace 'admin_app/register.html' with your template path


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Check username length and redirect accordingly
            if len(username) == 10 and username.startswith('23000'):
                return redirect('employee:homepage_employee')  # Replace 'student_home' with the URL name for the student app homepage
            elif len(username) == 4:
                return redirect('trainer:homepage_trainer')
                # Replace 'faculty_home' with the URL name for the faculty app
            elif username.startswith('admin') and len(username) == 10:
                return redirect('admin_app:homepage')
            else:
                messages.error(request, 'Username length does not match any role-specific redirects.')
                return redirect('admin_app:user_login')  # Redirect back to login if length does not match any criteria

        else:
            # If authentication fails, show an error message
            error_message = 'Invalid username or password. Please try again.'
            return render(request, 'admin_app/login.html', {'error_message': error_message})

    return render(request, 'admin_app/login.html')  # Render login page on GET request


@login_required
def log_out(request):
    # Use Django's built-in logout function
    logout(request)

    # Redirect to a specific page after logging out (e.g., login page or homepage)
    return redirect(reverse('admin_app:homepage'))

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UpdatePasswordForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile_page')
    else:
        form = UpdatePasswordForm(instance=request.user)
        messages.error(request, 'An error occurred While performing the Action')

    return render(request, 'admin_app/profile.html', {'form': form})


@login_required
def update_password(request):
    if request.method == 'POST':
        form = UpdatePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile_page')
        else:
            print(form.errors)  # For debugging
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UpdatePasswordForm(user=request.user)

    return render(request, 'admin_app/profile.html', {'password_form': form})

@login_required
def profile_page(request):
    return render(request, 'admin_app/profile.html', {
        'user': request.user,
    })


@login_required
def Course_Manage(request):
    return render(request, 'courses/base.html')

@login_required
def create_course_view(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_app:homepage')
    else:
        form = CourseForm()
        # Filter trainers with a username of exactly 4 characters
        form.fields['trainer'].queryset = User.objects.filter(username__regex=r'^\w{4}$')

    return render(request, 'courses/course_create.html', {'form': form})



@login_required
def delete_course_view(request, course_id):  # Use 'pk' instead of 'course_id' for standard naming
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        course.delete()
        messages.success(request, f'The course "{course.name}" was deleted successfully.')
        return redirect('admin_app:course_list')  # Redirect to the course list view after deletion

    return render(request, 'courses/course_delete.html', {'course': course})



@login_required
def update_course_view(request, course_id):  # Use 'id' to match your URL pattern
    # Fetch the course object using the id
    course = get_object_or_404(Course, id=course_id)
    trainers = User.objects.filter(username__regex=r'^\w{4}$')  # Filter trainers with username length 4

    if request.method == 'POST':
        # Updating the course details from POST data
        course.name = request.POST.get('name')
        course.description = request.POST.get('description')
        course.duration = request.POST.get('duration')
        course.trainer_id = request.POST.get('trainer')
        course.status = bool(request.POST.get('status'))

        # Save the updated course
        course.save()
        messages.success(request, f'Course "{course.name}" was updated successfully.')
        return redirect('admin_app:course_list')  # Redirect to the course list page or another page

    # Render the update course template
    return render(request, 'courses/course_edit.html', {'course': course, 'trainers': trainers})


@login_required
def course_list(request):
    courses = Course.objects.all()  # Get all courses
    return render(request, 'courses/course_list.html', {'courses': courses})
