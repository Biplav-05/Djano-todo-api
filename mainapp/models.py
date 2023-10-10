from django.db import models
from datetime import datetime
from django.utils import timezone
import random
from django.contrib.auth.models import AbstractUser,BaseUserManager,Group,Permission



class TodoModel(models.Model):
    title = models.CharField(max_length=50,blank=False)
    description = models.TextField(blank=False)
    date = models.DateTimeField(default=datetime.now)
    isComplete = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)


    

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=16,blank=True,null=True)
    otp_created_at = models.DateTimeField(blank=True,null=True)
    is_verified = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, blank=True, related_name='customuser_groups')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='customuser_user_permissions')


    objects = CustomUserManager()

    def generate_otp(self):
        otp = random.randint(100000,999999)
        self.otp = otp
        self.otp_created_at = timezone.now()
        self.save()
        return otp;

