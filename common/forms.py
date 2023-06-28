from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from pybo.models import Records
from common.models import CustomUser

class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    phone = forms.CharField(label="전화번호")
    nickname = forms.CharField(label="닉네임")
    address = forms.CharField(label="주소")
    class Meta:
        model = CustomUser  # CustomUser로 수정
        fields = ("username", "email", "phone", "nickname", "address")

class RecordsForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=[(str(i), str(i)) for i in range(1, 6)], label='별점')
    class Meta:
        model = Records
        fields = ['subject', 'content', 'rating', 'menu', 'food_name']
        widgets = {
            'subject': forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class':'form-control', 'rows': 10}),
        }

class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(label="성")
    last_name = forms.CharField(label="이름")
    email = forms.EmailField(label="이메일")
    phone = forms.CharField(label="전화번호")
    nickname = forms.CharField(label="닉네임")
    address = forms.CharField(label="주소")
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'nickname', 'username', 'phone', 'email', 'address']
