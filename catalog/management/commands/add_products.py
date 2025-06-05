from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Добавляет продукты в БД"

    def handle(self, *args, **kwargs):
        Category.objects.all().delete()
        Product.objects.all().delete()
        category, _ = Category.objects.get_or_create(
            name="Информационная безопасность",
            description="Комплекс решений для информационной безопасности компании",
        )
        products = [
            {
                "name": "Доступ",
                "description": "Настройка и обслуживание парка ПК для системных администраторов",
                "category": category,
                "price": 200000.00,
                "created_at": "2024-12-24",
            },
            {
                "name": "ID",
                "description": "Защита учетных записей сотрудников",
                "category": category,
                "price": 100000.00,
                "created_at": "2024-12-23",
            },
        ]

        for product in products:
            product, created = Product.objects.get_or_create(**product)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Продукт успешно добавлен: {product.name}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Продукт уже существует: {product.name}")
                )
