from django import forms
from django.db import models
from marks_system.models import *
from django.forms import ModelForm
from django.forms import ModelChoiceField
from django.contrib.auth import get_user_model
User = get_user_model()


class LoginForm(forms.Form):
    user_name = forms.CharField(required=True, label='Enter Username')
    password = forms.CharField(max_length=30, widget=forms.PasswordInput, label='Enter Password')

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        return cleaned_data


class UserCreationForm(forms.Form):
    user_name = forms.CharField(required=True, label='Enter Username')
    password = forms.CharField(max_length=30, widget=forms.PasswordInput, label='Enter Password')

    def clean(self):
        cleaned_data = super(UserCreationForm, self).clean()
        return cleaned_data

    def clean_user_name(self):
        user_name = self.cleaned_data['user_name'].strip()

        if len(user_name) < 3:
            raise forms.ValidationError("Enter more than 3 letters")

        User = get_user_model()
        if User.objects.filter(username=user_name).exists():
            raise forms.ValidationError("You entered user is already exists")
        return user_name


    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 5:
            raise forms.ValidationError("password is too short")
        return password


class DepartmentCreationForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'

    def clean(self):
        cleaned_data = super(DepartmentCreationForm, self).clean()
        return cleaned_data


class departmentModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return (obj.department_name)


class MarksAddForm(forms.ModelForm):
    department = departmentModelChoiceField(queryset=Department.objects.all())

    class Meta:
        model = StudentsMarks
        exclude = ['total_marks', 'created_by']

    def clean(self):
        cleaned_data = super(MarksAddForm, self).clean()
        return cleaned_data

    # User = get_user_model()
    # if StudentsMarks.objects.filter(student_name= student_name).exists():
    #     raise forms.ValidationError("You entered student is already exists")


class EditForm(forms.ModelForm):
    class Meta:
        model = StudentsMarks
        exclude = ['student_name','total_marks','created_by']

    def clean(self):
        cleaned_data = super(EditForm, self).clean()
        return cleaned_data