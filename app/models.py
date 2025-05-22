from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone
import datetime

class CustomUser(AbstractUser):
    title = models.CharField(max_length=100, blank=True, default='')
    address = models.TextField(blank=True, default='')
    phone = models.CharField(max_length=15, blank=True, default='')
    linkedin = models.CharField(max_length=150, blank=True, default='')
    twitter = models.CharField(max_length=150, blank=True, default='')
    instagram = models.CharField(max_length=150, blank=True, default='')
    dob=models.DateField(blank=True, default=datetime.date(2001, 1, 1))
    about = models.TextField(blank=True, default='',max_length=500)
    mapadd = models.TextField(blank=True, max_length=1000, default='')

    class ThemeChoices(models.IntegerChoices):
        THEME_1 = 1, 'Theme 1'
        THEME_2 = 2, 'Theme 2'
        THEME_3 = 3, 'Theme 3'
        THEME_4 = 4, 'Theme 4'

    theme = models.IntegerField(
        choices=ThemeChoices.choices,
        default=ThemeChoices.THEME_1,
    )

    paid = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group, related_name='customuser_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_permissions', blank=True)

    def __str__(self):
        return f"{self.username}"

class Info(models.Model):
    fk=models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='info')
    head=models.CharField(max_length=30)
    body=models.CharField(max_length=200)
    certificate=models.CharField(max_length=100,blank=True)
    linkedin=models.CharField(max_length=100,blank=True)

class Education(models.Model):
    fk=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name=models.CharField(max_length=25, null=True, blank=True)
    yearfrom=models.CharField(max_length=10, null=True, blank=True, default='')
    yearto=models.CharField(max_length=10, null=True, blank=True, default='')
    about=models.CharField(max_length=500, null=True, blank=True, default='')

class Experience(models.Model):
    fk=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name=models.CharField(max_length=25, null=True, blank=True)
    yearfrom=models.CharField(max_length=10, null=True, blank=True, default='')
    yearto=models.CharField(max_length=10, null=True, blank=True, default='')
    role=models.CharField(max_length=10, null=True, blank=True, default='')
    
class Skill(models.Model):
    fk=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    percentage = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.percentage}%)"

class Projects(models.Model):
    fk = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=25, blank=True)
    techused = models.CharField(max_length=10, blank=True, default='')
    description = models.TextField(blank=True, default='',max_length=500)
    image = models.ImageField(upload_to='project_images/', blank=True)

class News(models.Model):
    head=models.CharField(max_length=50)
    body=models.CharField(max_length=300)
    timex=models.DateTimeField(blank=True)

class Message(models.Model):
    fullname=models.CharField(max_length=50)
    email=models.EmailField(max_length=100)
    message=models.TextField(max_length=500)
    to=models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='message')
    time=models.DateTimeField(default=timezone.now)