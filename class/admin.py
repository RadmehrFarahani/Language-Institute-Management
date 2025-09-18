from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Language)
class LangAdmin(admin.ModelAdmin):
    list_display = ['lang_name']
    ordering = ['lang_name']
    list_filter = ['lang_name']
    search_fields = ['lang_name']
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name','lang_spec','year_of_teach','email']
    ordering = ['name','lang_spec']
    list_filter = ['name','lang_spec']
    list_editable = ['year_of_teach']
    search_fields = ['name']
@admin.register(Classes)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['title','level','language','teacher','start','status']
    ordering = ['level','language']
    list_filter = ['level','language','teacher','status']
    list_editable = ['teacher','status']
    search_fields = ['title','level','language']
@admin.register(Students)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name','stu_serial','lang_choices','class_choice']
    ordering = ['name','stu_serial']
    list_filter = ['lang_choices','class_choice']
    list_editable = ['lang_choices','class_choice']
    search_fields = ['name','stu_serial']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name','subject','email']






