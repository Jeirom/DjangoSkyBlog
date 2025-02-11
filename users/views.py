from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView

from users.forms import UserRegisterForm
from users.models import User


# Create your views here.
class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):

        user = form.save()  # Сохраняем пользователя
        # login(self.request, user)

        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'users:login'
    redirect_authenticated_user = True  # Перенаправление, если пользователь уже авторизован
    success_url = reverse_lazy('catalog:product_list')  # URL для перенаправления после успешного входа