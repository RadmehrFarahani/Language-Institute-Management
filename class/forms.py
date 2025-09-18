from venv import create
from .models import *
from django import forms

class ContactForm(forms.Form):
    SUBJECT=(
        ('گزارش','گزارش'),
        ('درخواست','درخواست'),
    )
    name = forms.CharField(max_length=250,required=True,label="نام و نام خانوادگی")
    subject=forms.ChoiceField(choices=SUBJECT,label='موضوع پیام')
    email = forms.EmailField(required=True,label='ایمیل')
    message=forms.CharField(max_length=400,widget=forms.Textarea,label='متن پیام')

class RegisterStudent(forms.ModelForm):
    class Meta:
        model=Students
        fields=['name','age','number','lang_choices','class_choice']

class RegisterClass(forms.ModelForm):
    class Meta:
        model=Classes
        fields=['title','language','level','teacher','sessions','start']

class RegisterTeacher(forms.ModelForm):
    class Meta:
        model=Teacher
        fields=['name','lang_spec','year_of_teach','email','number']

class SearchForm(forms.Form):
    query=forms.CharField()

class LoginForm(forms.Form):
   username=forms.CharField(max_length=250,required=True)
   password=forms.CharField(max_length=250,required=True,widget=forms.PasswordInput)