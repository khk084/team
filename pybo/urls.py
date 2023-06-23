from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    # path('', views.recommend_food, name='recommend_food'),

]