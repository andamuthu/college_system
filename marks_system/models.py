from django.db import models
from django.contrib.auth.models import AbstractUser
from django_currentuser.middleware import (get_current_user, get_current_authenticated_user)
from django_currentuser.db.models import CurrentUserField
from django.contrib.auth.models import Permission


class User(AbstractUser):
    is_superuser = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_principal = models.BooleanField(default=False)
    is_hod = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)


class Department(models.Model):
    department_name = models.CharField(max_length=100, unique=True)
    assign_hod = models.ForeignKey(User, on_delete=models.CASCADE)

    # staff = models.ForeignKey(User, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.department_name


class StudentsMarks(models.Model):
    student_name = models.CharField(max_length=100, unique=True)
    SEMESTER_CHOICES = (
    ("I", "I"), ("II", "II"), ("III", "III"), ("IV", "IV"), ("V", "V"), ("VI", "VI"), ("VII", "VII"),
    ("VIII", "VIII"),)
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES, default='1')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    tamil = models.IntegerField()
    english = models.IntegerField()
    maths = models.IntegerField()
    science = models.IntegerField()
    socialscience = models.IntegerField()
    total_marks = models.IntegerField()
    created_by = CurrentUserField()

    def __unicode__(self):
        return self.student_name

    def save(self, *args, **kwargs):
        self.total_marks = self.tamil + self.english + self.maths + self.science + self.socialscience
        super(StudentsMarks, self).save(*args, **kwargs)
