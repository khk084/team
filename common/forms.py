from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from pybo.models import Records
from common.models import CustomUser
import django.contrib.auth.forms as auth_forms

class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    phone = forms.CharField(label="전화번호")
    nickname = forms.CharField(label="닉네임")
    address = forms.CharField(label="주소")
    myname = forms.CharField(label="이름")
    class Meta:
        model = CustomUser  # CustomUser로 수정
        fields = ("username", "email", "phone", "nickname", "address", "myname")

class RecordsForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=[(str(i), str(i)) for i in range(1, 6)], label='별점')
    class Meta:
        model = Records
        fields = ['subject', 'content', 'rating', 'food_type', 'food_name']
        widgets = {
            'subject': forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class':'form-control', 'rows': 10}),
        }


class UserProfileForm(UserChangeForm):
    myname = forms.CharField(label="이름")
    email = forms.EmailField(label="이메일")
    phone = forms.CharField(label="전화번호")
    nickname = forms.CharField(label="닉네임")
    address = forms.CharField(label="주소")
    class Meta:
        model = CustomUser
        fields = ['myname', 'nickname', 'username', 'phone', 'email', 'address']

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = '기존 비밀번호'
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'autofocus': False,
        })
        self.fields['new_password1'].label = '새 비밀번호'
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['new_password2'].label = '새 비밀번호 확인'
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
        })

class PasswordResetForm(auth_forms.PasswordResetForm):
    username = auth_forms.UsernameField(label="사용자ID")  # CharField 대신 사용

    # validation 절차:
    # 1. username에 대응하는 User 인스턴스의 존재성 확인
    # 2. username에 대응하는 email과 입력받은 email이 동일한지 확인

    def clean_username(self):
        data = self.cleaned_data['username']
        if not CustomUser.objects.filter(username=data).exists():
            raise ValidationError("해당 사용자ID가 존재하지 않습니다.")

        return data

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")

        if username and email:
            if CustomUser.objects.get(username=username).email != email:
                raise ValidationError("사용자의 이메일 주소가 일치하지 않습니다")

    def get_users(self, email=''):
        active_users = CustomUser.objects.filter(**{
            'username__iexact': self.cleaned_data["username"],
            'is_active': True,
        })
        return (
            u for u in active_users
            if u.has_usable_password()
        )