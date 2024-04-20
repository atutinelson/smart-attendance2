from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class CustomUserManager(BaseUserManager):

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError("superuser has to have is_staff being true")

        if extra_fields.get('is_superuser') is not True:
            raise ValueError("superuser has to have is_superuser being true")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user





def set_default_time():
    now = datetime.now()
    return now.replace(year=2000, month=1, day=1, hour=1, minute=00, second=00)


class User(AbstractUser):
    email = models.CharField(max_length=80, unique=True)
    username = models.CharField(max_length=100)
    department = models.CharField(max_length=40)
    expo_token = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='media/', default="../media/media/1.jpg")

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',  'department']

    def __str__(self):
        return self.email


class Attendance(models.Model):
    time = models.DateTimeField(default=set_default_time)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance')

    def __str__(self):
        return f"{self.user}"


class Message(models.Model):
    title = models.CharField(max_length=100)
    message = models.CharField(max_length=5000000)
    posted_date = models.DateField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message')

    def __str__(self):
        return f"{self.title}"




