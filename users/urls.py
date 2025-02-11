from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, reverse_lazy
from users.models import User

from catalog.apps import CatalogConfig
from catalog.views import (ContactsView, ProductCreateView, ProductDeleteView,
                           ProductDetailView, ProductListView,
                           ProductUpdateView)
from users.views import UserCreateView, CustomLoginView

app_name = 'users'

urlpatterns = [
    path('login/', CustomLoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(template_name='register.html'), name='register')
]
