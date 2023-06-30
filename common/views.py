from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from common.forms import UserForm, UserProfileForm, CustomPasswordChangeForm, PasswordResetForm
from common.models import CustomUser
from pybo.models import Records
from django.db.models import Q
from django.core.paginator import Paginator
from django.urls import reverse_lazy

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

# 회원정보 보기
@login_required(login_url='common:login')
def profile_view(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    context = {'user': user}
    return render(request, 'common/profile_view.html', context)

# 회원정보 수정
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


# 회원정보 보기에서 비밀번호 변경
@login_required(login_url='common:login')
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # 비밀번호 변경 후에 자동 로그인
            messages.success(request, '패스워드가 변경되었습니다!')
            return redirect('common:profile_view', user_id=request.user.id)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'common/change_password.html', {
        'form': form
    })

class PasswordResetView(auth_views.PasswordResetView):
    """
    비밀번호 초기화 - 사용자ID, email 입력
    """
    template_name = 'common/password_reset.html'
    success_url = reverse_lazy('common:password_reset_done')
    form_class = PasswordResetForm
    # email_template_name = 'common/password_reset_email.html'


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    """
    비밀번호 초기화 - 메일 전송 완료
    """
    template_name = 'common/password_reset_done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    """
    비밀번호 초기화 - 새로운 비밀번호 입력
    """
    template_name = 'common/password_reset_confirm.html'
    success_url = reverse_lazy('common:login')
