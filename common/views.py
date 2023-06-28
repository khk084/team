from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from common.forms import UserForm, UserProfileForm
from common.models import CustomUser

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
