from django.contrib.admin.templatetags.admin_list import results
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse, Http404
from pyexpat.errors import messages
from .models import *  # Ensure correct model names
from .forms import *
from django.views.generic import ListView,DetailView
from django.core.paginator import Paginator
# from django.contrib.postgres.search import SearchVector
# from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

def index(request):
    return render (request,'class/index.html')
# Create your views here.
###############1#################
@login_required
def classes(request):
    classes = Classes.objects.filter(status=Classes.Status.REGISTERING)
    paginator=Paginator(classes,3)
    page_number=request.GET.get('page',1)
    classes=paginator.page(page_number)
    context = {
        'classes': classes,
    }
    return render(request, "class/class_list.html", context)


# class ClassList(ListView):
#     model = Classes
#     context_object_name = "classes"
#     template_name = "class/class_list.html"


###############2#################
def class_list(request, id):
    detail= get_object_or_404(Classes,id=id,status=Classes.Status.REGISTERING)
    context = {
        'detail': detail,
    }
    return render(request, "class/class_detail.html", context)
# class ClassDetail(DetailView):
#     model = Classes
#     template_name = "class/class_detail.html"

###############3#################
@login_required
def teachers(request):
    teachers = Teacher.objects.all()
    paginator=Paginator(teachers,3)
    page_number=request.GET.get('page',1)
    teachers=paginator.page(page_number)
    context = {
        'teachers': teachers
    }
    return render(request, "class/teacher.html", context)

# class TeacherList(ListView):
#     model = Teacher
#     context_object_name = "teachers"
#     template_name = "class/teacher.html"

###############4#################
def teacher_detail(request, id):
    teach_detail= get_object_or_404(Teacher,id=id)
    context = {
        'teach_detail': teach_detail,
    }
    return render(request, "class/teacher_detail.html", context)

# class TeacherDetail(DetailView):
#     model = Teacher
#     template_name = "class/teacher_detail.html"
#     context_object_name = "teach_detail"

###############5#################
@login_required
def students(request):
    students = Students.objects.all()
    paginator=Paginator(students,3)
    page_number=request.GET.get('page',1)
    students=paginator.page(page_number)
    context = {
        'students': students
    }
    return render(request, "class/student.html", context)

# class StudentList(ListView):
#     model = Students
#     context_object_name = "students"
#     template_name = "class/student.html"

###############6#################

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            text_obj=Contact.objects.create(  # Use the model here, not the form
                name=cd['name'],
                subject=cd['subject'],
                email=cd['email'],
                message=cd['message']
            )
            return redirect("class:contact")
    else:
        form = ContactForm()

    return render(request, "forms/contact.html", {'form': form})

###############7#################
@login_required
def register_student(request):
    if request.method == "POST":
        form = RegisterStudent(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            form_obj=Students.objects.create(  # Use the model here, not the form
                name=cd['name'],
                stu_serial='00000',
                age=cd['age'],
                number=cd['number'],
                lang_choices=cd['lang_choices'],
                class_choice=cd['class_choice']
            )
            return redirect("class:register")

    else:
        form = RegisterStudent()

    return render(request, "forms/register_student.html", {'form': form})
###############8#################
@login_required
def contact_list(request):
    message=Contact.objects.all()
    context={
        'message':message
    }
    return render(request,'class/contact_list.html',context)

###############9#################
@login_required
def contact_detail(request, id):
    contact_detail= get_object_or_404(Contact,id=id)
    context = {
        'contact_detail': contact_detail ,
    }
    return render(request, "class/contact_detail.html", context)

###############10#################
@login_required
def search(request):
    query=None
    result=[]
    if 'query' in request.GET:
        form=SearchForm(data=request.GET)
        if form.is_valid():
            query=form.cleaned_data['query']
            # result=(Classes.objects.annotate(search=SearchVector('title','level'))
            #         .filter(search=query))

            result= (Classes.objects.annotate(similarity=TrigramSimilarity("title",query))
                      .filter(similarity__gt=0.1)).order_by('-similarity')

    context={
        'query':query,
        'result' : result
    }

    return render(request,'class/search.html',context)


# def profile(request):
#     class_li=Classes.objects.all()
#     student=Students.objects.all()
#     teacher=Teacher.objects.all()
#     context={
#         'class_li':class_li,
#         'student':student,
#         'teacher':teacher
#
#     }
#     return render(request,'class/profile.html',context)
#

@login_required
def profile(request):
    if request.user.is_authenticated:
        class_li = Classes.objects.all()
        student = Students.objects.all()
        teacher = Teacher.objects.all()
    else:
        class_li = Classes.objects.none()
        student = Students.objects.none()
        teacher = Teacher.objects.none()

    context={
        'class_li':class_li,
        'student':student,
        'teacher':teacher
    }
    return render(request, 'class/profile.html', context)
@login_required
def add_class(request):
    if request.method == "POST":
        form = RegisterClass(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            form_obj=Classes.objects.create(  # Use the model here, not the form
                title=cd['title'],
                language=cd['language'],
                level=cd['level'],
                teacher=cd['teacher'],
                sessions=cd['sessions'],
                start=cd['start']
            )
            return redirect("class:profile")

    else:
        form = RegisterClass()

    return render(request, "forms/add_class.html", {'form': form})

@login_required
def register_teacher(request):
    if request.method == "POST":
        form = RegisterTeacher(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            form_obj=Teacher.objects.create(  # Use the model here, not the form
                name=cd['name'],
                lang_spec=cd['lang_spec'],
                year_of_teach=cd['year_of_teach'],
                email=cd['email'],
                number=cd['number'],
            )
            return redirect("class:profile")

    else:
        form = RegisterTeacher()

    return render(request, "forms/register_teacher.html", {'form': form})
@login_required
def delete_class(request,id):
    class_obj=get_object_or_404(Classes,id=id)
    if request.method == "POST":
        class_obj.delete()
        return redirect('class:profile')
    return render(request, 'forms/delete_class.html', {'class_obj': class_obj})
@login_required
def edit_class(request,id):
    Edclass = get_object_or_404(Classes, id=id)
    if request.method== "POST" :
        form=RegisterClass(request.POST, instance=Edclass)
        if form.is_valid :
            Edclass=form.save(commit=False)
            Edclass.save()
            return redirect('class:profile')
    else:
        form=RegisterClass(instance=Edclass)

    return render(request,'forms/add_class.html',{'Edclass':Edclass, 'form':form})

def user_login(request):
    if request.method == "POST":
        form=LoginForm(request.POST)
        if form.is_valid() :
            cd=form.cleaned_data
            user=authenticate(request,username=cd['username'],password=cd['password'])
            if user is not None :
                if user.is_active:
                    login(request, user)
                    return redirect('class:profile')
                else :
                    return HttpResponse("Your account is disabled")
            else:
                return HttpResponse("You are not logged in")
    else:
        form=LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))
# ////////////////////////////////////////////////////////
# def register(request):
#     if request.method == "POST":
#         form = RegisterStudent(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             Students.objects.create(
#                 name=cd['name'],
#                 stu_serial='00000',
#                 age=cd['age'],
#                 number=cd['number'],
#                 lang_choices=cd['lang_choices'],
#                 class_choice=cd['class_choice']
#             )
#             return redirect("class:register")
#     else:
#         form = RegisterStudent()
#
#     # اگر زبان انگلیسی انتخاب شده بود، فیلتر کلاس‌ها رو اعمال کن
#     lang = None
#     if request.method == "POST":
#         lang = request.POST.get('lang_choices')
#     else:
#         # اگر خواستی حالت پیش‌فرض بذاری
#         lang = None
#
#     if lang == 'english':  # یا مقدار دقیق که برای انگلیسی توی گزینه‌ها گذاشتی
#         # فرض می‌کنم مدل کلاس‌ها ClassModel هست و فیلد رشته‌ش 'major' یا مشابهش هست
#         filtered_classes = ClassModel.objects.filter(major__iexact='english')
#     else:
#         filtered_classes = ClassModel.objects.all()
#
#     # حالا فرم رو با کوئریست کلاس‌های فیلتر شده مقداردهی کن
#     form.fields['class_choice'].queryset = filtered_classes
#
#     return render(request, "forms/register_student.html", {'form': form})

