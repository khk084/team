from django.db import models
from common.models import CustomUser

# Create your models here.
class Food(models.Model):
    foodname = models.CharField(max_length=100)
    foodtype = models.CharField(max_length=100)
    foodprice = models.CharField(max_length=100)
    def __str__(self):
        return self.foodname


class Records(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, null=True)
    food_name = models.CharField(max_length=100, blank=True, null=True)  # 음식 이름
    menu = models.CharField(max_length=100, blank=True, null=True)  # 음식 타입
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    subject = models.CharField(max_length=100)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    rating = models.IntegerField(blank=True, null=True) # 별점
    def __str__(self):
        return self.subject

    @property
    def food_menu(self):
        return self.food.foodname if self.food else ""