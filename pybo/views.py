from django.shortcuts import render
import random

from django.shortcuts import render
from django.shortcuts import redirect
from .models import Food, Records
from common.forms import RecordsForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.


def index(request):
    return render(request, 'main.html')

def login_page(request):
    """
    로그인 페이지
    """
    return render(request, 'login.html')


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
            records.food_name = request.GET.get('food_name')  # Get the menu value from URL parameters
            records.menu = request.GET.get('food_menu')
            records.save()
            return redirect('index')
    else:
        form = RecordsForm()
    context = {'form': form}
    return render(request, 'pybo/records_form.html', context)

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
