from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .form import UserForm
from django.http import HttpResponse
from .models import Food
import random
# Create your views here.


def index(request):
    return render(request, 'base.html')

def login_page(request):
    """
    로그인 페이지
    """
    return render(request, 'login.html')

# 회원가입
def signup(request):
    """
    회원가입 페이지
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'signup.html', {'form': form})

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


