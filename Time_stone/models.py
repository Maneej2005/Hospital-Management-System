from django.db import models

# Create your models here.

class Student(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField()

class college(models.Model):

    reg = models.IntegerField()
    name = models.CharField(max_length=50)
    phno = models.CharField(max_length=10)
