import secrets
import logging
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from users.forms import UserRegisterForm
from users.models import User
from config.settings import EMAIL_HOST_USER


logging.basicConfig(level=logging.DEBUG)

# Create your views here.
class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):

        user = form.save()  # Сохраняем пользователя
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        logging.debug(f'Токен: {token}')
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject='Спасибо за регистрацию!',
            message=f'Для завершения регистрации на SkyShop подтвердите Вашу почту --> {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)

def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))

class CustomLoginView(LoginView):
    template_name = 'users:login'
    redirect_authenticated_user = True  # Перенаправление, если пользователь уже авторизован
    success_url = reverse_lazy('catalog:product_list')  # URL для перенаправления после успешного входа

    def form_valid(self, form):

        return super().form_valid(form)
