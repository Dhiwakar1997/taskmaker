from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUsers(AbstractUser):
    name = models.CharField(max_length=50,default='Anonymous')
    email = models.EmailField(max_length=254,unique=True,blank=False)

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    phone=models.CharField(max_length=30,blank=True,null=True)
    gender=models.CharField(max_length=10,blank=True,null=True)
    profile_pic = models.ImageField(upload_to='users/profile_pics',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    passwordResetToken=models.CharField(max_length=50,blank=True,null=True)
    passwordResetTime=models.DateTimeField(blank=True,null=True)
    ROLES=(('admin','Admin'),('QC','Quality Checker'),('designer','Designer'))
    role=models.CharField(max_length=8,choices=ROLES,blank=True)
    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.name
