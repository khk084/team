from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from common.forms import UserForm, UserProfileForm
from common.models import CustomUser
from pybo.models import Records
from django.db.models import Q
from django.core.paginator import Paginator


# Create your views here.
# 회원가입
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            address = form.cleaned_data.get('address')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})

@login_required(login_url='common:login')
def profile_view(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    context = {'user': user}
    return render(request, 'common/profile_view.html', context)

@login_required(login_url='common:login')
def profile_update(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '회원정보가 수정되었습니다')
            return redirect('common:profile_view', user_id=user_id)
    else:
        form = UserProfileForm(instance=request.user)

    context = {'user': user, 'form': form}
    return render(request, 'common/profile_update.html', context)

@login_required(login_url='common:login')
def profile_record(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    records_list = Records.objects.filter(author=request.user)  # 로그인한 사용자와 관련된 모든 레코드를 가져옵니다

    # 기록 정렬 및 검색 기능 추가
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    so = request.GET.get('so', 'recent')

    if so == 'recommend':
        records_list = records_list.order_by('rating', '-create_date')
    elif so == 'views':
        records_list = records_list.order_by('-views', '-create_date')
    else:  # 최신순
        records_list = records_list.order_by('-create_date')

    if kw:
        records_list = records_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(menu__icontains=kw) |
            Q(author__username__icontains=kw)
        ).distinct()

    paginator = Paginator(records_list, 5)  # 페이지당 숫자만큼 게시물 보여줌
    page_obj = paginator.get_page(page)

    context = {
        'user': user,
        'records_list': page_obj,
    }


    return render(request, 'common/profile_records.html', context)


