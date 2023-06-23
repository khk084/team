from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    phone = forms.CharField(label="전화번호")
    nickname = forms.CharField(label="닉네임")
    address = forms.CharField(label="주소")

    class Meta:
        model = User
        fields = ("username", "email", "phone", "nickname", "address")