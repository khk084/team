from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name= 'common'

urlpatterns =[
    path('login/', auth_views.LoginView.as_view(
        template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile_view/<int:user_id>/', views.profile_view, name='profile_view'),
    path('profile_update/<int:user_id>/', views.profile_update, name='profile_update'),
    path('profile_records/<int:user_id>', views.profile_record, name='profile_record'),
    path('password_change/', views.change_password, name='change_password'),


    # 비밀번호 찾기를 위한 url 시작
    path('password_reset/', views.PasswordResetView.as_view(), name="password_reset"),
    path('password_reset_done/', views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

]