from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('records/', views.records, name="records"),
    path('<int:records_id>/', views.records_detail, name="re_detail"),
    path('records/<int:records_id>/submit-rating/', views.submit_rating, name='submit_rating'),
    # path('', views.recommend_food, name='recommend_food'),
]