from ast import Expression
import email
from pyexpat import model
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class user(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=False,)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    bio = models.CharField(max_length=900)
    expression = models.CharField(max_length=10)
    profile_pic = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.name
            