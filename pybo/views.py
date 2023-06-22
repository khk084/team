from django.shortcuts import render
from django.http import HttpResponse
from .models import Food
import random
# Create your views here.

def index(request) :
    return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.")

def recommend_food(request):
    #모든 음식 조회
    all_food = Food.objects.all()

    # 음식이 존재하지 않을 경우에 대한 예외 처리

    if not all_food:
        return render(request, 'pybo/no_food.html')

    # 랜덤한 음식을 선택
    random_food = random.choice(all_food)

    context = {
        'food': random_food
    }

    return render(request, 'pybo/recommend_food.html', context)
