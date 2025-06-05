from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email', help_text='Указанный почтовый адрес будет использоваться для авторизации на сайте.')
    image = models.ImageField(upload_to='users/avatars/',verbose_name='Аватар', blank=True, null=True, help_text='Добавьте свой аватар. Необязательное поле.')
    phone = models.CharField(max_length= 15, unique=True, verbose_name='Номер телефона', blank=True, null=True, help_text='Введите ваш номер телефона. Необязательное поле.')
    country = models.CharField(verbose_name='Ваша страна при регистрации', blank=True, null=True)
    token = models.CharField(max_length=100, verbose_name='Token', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


    def __str__(self):
        return self.email