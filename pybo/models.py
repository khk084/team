from django.db import models
from common.models import CustomUser

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


class Records(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    subject = models.CharField(max_length=100)
    content = models.TextField()
    create_date = models.DateTimeField()
    rating = models.IntegerField(blank=True, null=True)  # 별점
    def __str__(self):
        return self.subject
