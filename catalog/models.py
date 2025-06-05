from django.db import models
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название категории")
    description = models.TextField(verbose_name="Описание категории")

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название продукта")
    description = models.TextField(verbose_name="Описание продукта")
    photo = models.ImageField(
        upload_to="catalog/photo",
        blank=True,
        null=True,
        verbose_name="Фото",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория",
        blank=True,
        null=True,
        related_name="categories",
    )
    price = models.FloatField(verbose_name="Цена за покупку")
    created_at = models.DateField(
        verbose_name="Дата создания записи", blank=True, null=True
    )
    updated_at = models.DateTimeField(
        verbose_name="Дата последнего изменения", blank=True, null=True
    )
    public_status = models.BooleanField(default=False) # Статус публикации. По умолчанию = False. Когда модератор поменяет статус на True - продукт появится на сайте
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True) # Связывает продукцию к определенному пользователю *который авторизован на сайте

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = ["name"]
        permissions = [
            ('can_unpublish_product', 'Can unpublish product'),
        ]
    def __str__(self):
        return f"{self.name}"


class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя контакта")
    country = models.TextField(verbose_name="Страна")

    class Meta:
        verbose_name = "контакт"
        verbose_name_plural = "контакты"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name, self.country}"
