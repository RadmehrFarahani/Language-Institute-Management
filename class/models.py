from django.utils import timezone
from django.db import models
from django.urls import reverse

# Create your models here.
#Languages Table
class Language(models.Model):
    class Lang(models.TextChoices):
        ENGLISH = "EN", "English"
        FRENCH = "FC", "French"
        GERMANY = "GR", "Germany"
        ITALIAN= "IT" , "Italian"
        SPAIN= "SP" , "Spain"
        ARABIC= "AR" , "Arabic"
    lang_name = models.CharField(max_length=2,choices=Lang.choices,default=Lang.ENGLISH)
    def __str__(self):
        return f"{self.lang_name}"

#Teachers Table
class Teacher(models.Model):
    name=models.CharField(max_length=400)
    year_of_teach=models.IntegerField()
    email=models.EmailField()
    number=models.CharField(max_length=12)
    lang_spec=models.ForeignKey(Language,on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name}"

#Classes Table
class Classes(models.Model):
    class Status(models.TextChoices):
        REGISTERING = "RG", "Registering"
        STARTED = "ST", "Started"
        CANCELED = "CN", "Canceled"
    class Level(models.TextChoices):
        BASIC = "BC", "Basic"
        INTERMEDIATE = "IN", "Intermediate"
        ADVANCE = "AV", "Advance"
    title = models.CharField(max_length=100)
    level=models.CharField(max_length=2,choices=Level.choices,default=Level.BASIC)
    sessions=models.IntegerField()
    status=models.CharField(max_length=2,choices=Status.choices,default=Status.REGISTERING)
    start=models.DateField(default=timezone.now)
    language=models.ForeignKey(Language, on_delete=models.CASCADE)
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ["-level" , "-start"]
    def get_absolute_url(self):
        return reverse('class:class_detail',args=[self.id])



# Students Table
class Students(models.Model):
    class Level(models.TextChoices):
        BASIC = "BC", "Basic"
        INTERMEDIATE = "IN", "Intermediate"
        ADVANCE = "AV", "Advance"
    name = models.CharField(max_length=400)
    stu_serial = models.CharField(max_length=14)
    level = models.CharField(max_length=2, choices=Level.choices, default=Level.BASIC)
    number = models.CharField(max_length=12)
    age = models.CharField(max_length=12)
    lang_choices=models.ForeignKey(Language, on_delete=models.CASCADE,null=True)
    class_choice = models.ForeignKey(Classes, on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=250)
    subject=models.CharField(max_length=100)
    email = models.EmailField()
    message=models.CharField(max_length=400)
    class Meta:
        verbose_name="پیام"
        verbose_name_plural="پیام ها"


    def __str__(self):
        return self.subject
