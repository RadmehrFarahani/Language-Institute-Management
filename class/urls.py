from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name="class"

urlpatterns=[
    path('',views.index,name="index"),
    path('class/',views.classes,name="list_class"),
    path('class/<int:id>',views.class_list,name="class_detail"),
    path('teachers/',views.teachers,name="list_teachers"),
    path('teachers/<int:id>',views.teacher_detail,name="teacher_detail"),
    path('students/',views.students,name="list_students"),
    path('contact/',views.contact,name="contact"),
    path('messages/',views.contact_list,name="contact_list"),
    path('messages/<int:id>',views.contact_detail,name="contact_detail"),
    path('search/',views.search,name="search"),
    path('profile/',views.profile,name="profile"),
    path('profile/add_class',views.add_class,name="add_class"),
    path('profile/delete_class/<int:id>',views.delete_class,name="delete_class"),
    path('profile/edit_class/<int:id>', views.edit_class, name='edit_class'),
    path('profile/register_teacher',views.register_teacher,name="register_teacher"),
    path('profile/register_student',views.register_student,name="register_student"),
    path('login/', views.user_login, name='login'),
    path('logout/', views.log_out , name='logout'),

]