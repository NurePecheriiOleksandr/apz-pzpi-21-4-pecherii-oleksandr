"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Add password field
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    height = models.FloatField(blank=True, null=True)
    foot_size = models.IntegerField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


#Other Models
class Massage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    massage_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.text

class Organizer(models.Model):
    organizer_name = models.CharField(max_length=100)
    organizer_type = models.CharField(max_length=100)
    def __str__(self):
        return self.organizer_name

class Gear(models.Model):
    gear_name = models.CharField(max_length=100)
    gear_type = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)    
    def __str__(self):
        return self.gear_name

class DiveComputer(models.Model):
    depth = models.FloatField()
    dive_time = models.IntegerField()

class Activity(models.Model):
    activity_name = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100)
    description = models.TextField()
    places = models.IntegerField()
    activity_date_time = models.DateTimeField(auto_now_add=True)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)   
    def __str__(self):
        return self.activity_name

class Participation(models.Model):
    group = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dive_computer = models.ForeignKey(DiveComputer, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    gear = models.ForeignKey(Gear, on_delete=models.CASCADE)
    def __str__(self):
        return self.group