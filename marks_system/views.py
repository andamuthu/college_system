from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from marks_system.models import *
from marks_system.forms import *
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

from django_currentuser.middleware import (get_current_user, get_current_authenticated_user)
# from django.contrib.auth import get_user_model
# User = get_user_model()


from django.urls import reverse
from django.shortcuts import render, redirect
from marks_system.models import *
from marks_system.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django_currentuser.middleware import (get_current_user)


def index(request):
    return render(request, 'index.html')


def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'login_form': LoginForm()})
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name'].strip()
            password = form.cleaned_data['password'].strip()
            user = authenticate(username=user_name, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('marks_system:dashboard'))
            else:
                message = 'Invalid username/password'
                return render(request, "login.html",
                              {'message': message, 'login_form': form})
        else:
            message = 'Please correct below errors'
            return render(request, "login.html",
                          {'message': message, 'login_form': form})


@login_required(login_url='marks_system:login')
def dashboard(request):
    if request.method == 'GET':
        return render(request, "dashboard.html", )


def logout_view(request):
    user = request.user
    logout(request)
    return render(request, 'logout.html', {'user': user})


@login_required(login_url='marks_system:login')
def user_creation(request):
    if request.method == 'GET':
        return render(request, 'user_creation.html', {'UserCreationForm': UserCreationForm(), })
    elif request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name'].strip()
            password = form.cleaned_data['password'].strip()
            # user_type = form.cleaned_data['user_type'].strip()
            user_type = request.POST['user_type']

            if user_type == 'superadmin':
                user = User.objects.create(username=user_name, is_superadmin=True, )
            elif user_type == 'principal':
                user = User.objects.create(username=user_name, is_principal=True)
            elif user_type == 'HOD':
                user = User.objects.create(username=user_name, is_hod=True)
            elif user_type == 'Staff':
                user = User.objects.create(username=user_name, is_staff=True)
            elif user_type == 'Student':
                user = User.objects.create(username=user_name, is_student=True)

            else:
                message = 'Please select user type'
                return render(request, "user_creation.html",
                              {'message': message, 'UserCreationForm': form})

            user.set_password(password)
            user.save()
            message = 'User name " {} " is registred successfully'.format(user_name)
            form = UserCreationForm()
            return render(request, "user_creation.html",
                          {'message': message, 'UserCreationForm': form})
        else:
            message = 'Please correct below errors'
            return render(request, "user_creation.html",
                          {'message': message, 'UserCreationForm': form})


def department_creation(request):
    if request.method == 'GET':
        form = DepartmentCreationForm()
        return render(request, 'add_departments.html', {'departmentcreationform': form}, )
    elif request.method == 'POST':
        form = DepartmentCreationForm(request.POST)
        if form.is_valid():
            department_name = form.cleaned_data['department_name'].strip()
            assign_hod = form.cleaned_data['assign_hod']
            Department.objects.create(department_name=department_name, assign_hod=assign_hod)
            form = DepartmentCreationForm()
            message = '"{}" Department added successfully'.format(department_name)
            return render(request, 'add_departments.html', {'message': message, 'departmentcreationform': form})
        else:
            message = 'Please correct below errors'
            return render(request, "add_departments.html",
                          {'message': message, 'departmentcreationform': form})


def students_list():
    user = get_current_user()
    if user.is_superuser or user.is_superadmin or user.is_principal:
        return StudentsMarks.objects.all()
    elif user.is_hod:
        department = Department.objects.get(assign_hod_id=user.id)
        user_department = department.id
        return StudentsMarks.objects.filter(department=user_department)
    elif User.is_staff:
        return StudentsMarks.objects.filter(created_by=get_current_user())
    elif user.is_student:
        return StudentsMarks.objects.filter(student_name=user)


@login_required(login_url='marks_system:login')
def students_marklist(request):
    return render(request, 'student_name_list.html', {'students_list': students_list()})


@login_required(login_url='marks_system:login')
def add_students_marks(request):
    if request.method == 'GET':
        form = MarksAddForm()
        return render(request, 'add_marks.html', {'add_marks_form': form})
    elif request.method == 'POST':
        form = MarksAddForm(request.POST)
        if form.is_valid():
            student_name = form.cleaned_data['student_name'].strip()
            semester = form.cleaned_data['semester'].strip()
            department = form.cleaned_data['department']
            tamil = form.cleaned_data['tamil']
            english = form.cleaned_data['english']
            maths = form.cleaned_data['maths']
            science = form.cleaned_data['science']
            socialscience = form.cleaned_data['socialscience']
            total_marks = tamil + english + maths + science + socialscience
            StudentsMarks.objects.create(student_name=student_name, semester=semester, department=department,
                                         tamil=tamil, english=english,
                                         maths=maths, science=science, socialscience=socialscience,
                                         total_marks=total_marks)
            message = ' " {} " marks are added successfully'.format(student_name)
            return render(request, 'student_name_list.html', {'message': message, 'students_list': students_list()})
        else:
            message = 'Please correct below errors'
            return render(request, 'add_marks.html', {'message': message, 'add_marks_form': MarksAddForm()})


def edit_marks(request, pk):
    if request.method == 'GET':
        edit_student = StudentsMarks.objects.get(id=pk)
        form = EditForm(instance=edit_student)
        return render(request, 'edit_marks.html',
                      {'edit_student': edit_student, 'editform': form})
    elif request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            semester = form.cleaned_data['semester'].strip()
            department = form.cleaned_data['department']
            tamil = form.cleaned_data['tamil']
            english = form.cleaned_data['english']
            maths = form.cleaned_data['maths']
            science = form.cleaned_data['science']
            socialscience = form.cleaned_data['socialscience']
            mark_update = StudentsMarks.objects.get(id=pk)
            # update(tamil=tamil, english=english, science=science, socialscience=socialscience, )
            mark_update.semester = semester
            mark_update.department = department
            mark_update.tamil = tamil
            mark_update.english = english
            mark_update.maths = maths
            mark_update.science = science
            mark_update.socialscience = socialscience
            mark_update.save()
            message = ' " {} " marks are updated successfully'.format(mark_update.student_name)
            return render(request, 'student_name_list.html',
                          {'message': message, 'students_list': students_list(), })
        else:
            message = 'Form is not valid'
            edit_student = StudentsMarks.objects.get(id=pk)
            form = EditForm(instance=edit_student)
            return render(request, 'edit_marks.html',
                          {'message': message, 'edit_student': edit_student, 'editform': form})


def delete_student(request, pk):
    student = StudentsMarks.objects.get(id=pk)
    student.delete()
    message = ' "{}"  Student is deleted successfully'.format(student.student_name)
    return render(request, 'student_name_list.html',
                  {'message': message, 'students_list': students_list(), })
