from django.db import models
from django.utils import timezone
import random
from django.contrib.auth.models import AbstractUser,BaseUserManager,Group,Permission

class CustomUserManager(BaseUserManager):
    def create_user(self, email, firstname,lastname, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, firstname=firstname,lastname = lastname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, firstname,lastname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, firstname, lastname, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    is_verified = models.BooleanField(default=False)
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
    groups = models.ManyToManyField(Group, blank=True, related_name='customuser_groups')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='customuser_user_permissions')

    objects = CustomUserManager()
    
class OTP(models.Model):
    user = models.OneToOneField(CustomUser,on_delete= models.CASCADE,blank=True,null=True,related_name='OTP')
    otp = models.CharField(max_length=16,blank=True,null=True)
    otp_created_at = models.DateTimeField(blank=True,null=True,auto_now_add=True)
    
    
    def generate_otp(self):
        print("Before generate: ", self.otp)
        otp = OtpGenerator.generate_otp()
        self.otp = otp
        self.otp_created_at = timezone.now()
        self.save()
        print("After generate: ", self.otp)
        return otp

    def is_otp_verified(self):
        if self.otp and self.otp_created_at:
            timediffernces  = timezone.now() - self.otp_created_at
            if timediffernces.total_seconds() <=300:
                return True
        return False
    
    def reset_otp(self):
        self.otp = None;
        self.otp_created_at = None
        self.save()
  
    def __str__(self):
        return f"otp for user {self.user} is {self.otp}";

class OtpGenerator:
    def generate_otp():
        return str(random.randint(100000, 999999))