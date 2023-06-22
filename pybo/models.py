from django.db import models

# Create your models here.

class Suggestion(models.Model):
    fName=models.CharField(max_length=200)
    fMenu=models.CharField(max_length=200)
    select_date = models.DateTimeField()

class Food(models.Model):
    name = models.CharField(max_length=100)
    menu = models.CharField(max_length=100)
    price = models.CharField(max_length=100)

def __str__(self):
    return self.name
