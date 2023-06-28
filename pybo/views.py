import random

from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from .models import Food, Records
from common.forms import RecordsForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    return render(request, 'main.html')

def login_page(request):
    """
    로그인 페이지
    """
    return render(request, 'login.html')


def recommend_food(request):
    food_type = request.GET.get('food_type')
    #모든 음식 조회
    foods = Food.objects.all()

    # 음식이 존재하지 않을 경우에 대한 예외 처리

    if not foods.exists():
        return render(request, 'pybo/no_food.html')

    # 특정 분류의 음식이 선택되었을 경우
    if food_type:
        foods = foods.filter(foodtype=food_type)

    # 랜덤한 음식을 선택
    random_food = random.choice(foods)

    context = {
        'food_name': random_food.foodname,
        'food_type': random_food.foodtype,
        'food_price': random_food.foodprice,
    }

    return render(request, 'recommend.html', context)


def records(request):
    # 기록보기
    records_list = Records.objects.order_by('-create_date')
    context = {'records_list': records_list}
    return render(request, 'pybo/records_list.html', context)

def records_detail(request, records_id):
    # 기록보기 상세
    records = Records.objects.get(id=records_id)
    context = {'records': records}
    return render(request, 'pybo/records_detail.html', context)

def submit_rating(request, records_id):
    # 별점 등록
    if request.method == "POST":
        rating = request.POST.get('rating')
        records = Records.objects.get(id=records_id)
        records.rating = rating
        records.save()
        return redirect('re_detail', records_id=records_id)

    return redirect('re_detail', records_id=records_id)

@login_required(login_url='common:login')
def records_create(request):
    # 글쓰기
    if request.method == 'POST':
        form = RecordsForm(request.POST)
        if form.is_valid():
            records = form.save(commit=False)
            records.author = request.user
            records.create_date = timezone.now()
            records.food_name = request.GET.get('food_name')
            records.menu = request.GET.get('food_menu')
            records.save()
            return redirect('records')
    else:
        form = RecordsForm()
    context = {'form': form}
    return render(request, 'pybo/records_form.html', context)

@login_required(login_url='common:login')
def records_modify(request, records_id):
    # 글쓰기 수정
    records = get_object_or_404(Records, pk=records_id)
    if request.user != records.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('re_detail', records_id=records.id)

    if request.method == "POST":
        form = RecordsForm(request.POST, instance=records)
        if form.is_valid():
            records = form.save(commit=False)
            records.author = request.user
            records.modify_date = timezone.now()
            records.save()
            return redirect('re_detail', records_id=records.id)
    else:
        form = RecordsForm(instance=records, initial={
            'menu': records.menu,
            'food_name': records.food_name
        })
    context = {'form': form}
    return render(request, 'pybo/records_form.html', context)
    
@login_required(login_url='common:login')
def records_delete(request, records_id):
    # 글쓰기 삭제
    records = get_object_or_404(Records, pk=records_id)
    if request.user != records.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('re_detail', records_id=records_id)
    records.delete()
    return redirect('records')

def recommend(request):
    """
    추천 페이지
    """
    return render(request,'recommend.html')

def test(request):
    """
    index test 페이지
    """
    return render(request,'test/main2.html')
