from django.contrib.auth.views import LogoutView
from django.urls import path
from users.views import UserCreateView, CustomLoginView, email_verification

app_name = 'users'

urlpatterns = [
    path('login/', CustomLoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(template_name='register.html'), name='register'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm')
]


