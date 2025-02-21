from catalog.models import Product
from config.settings import CACHE_ENABLED
from django.core.cache import cache


def get_products_by_category(category_name):
    """Функция возвращает список продуктов по заданной категории"""
    products = Product.objects.filter(category=category_name)
    return products


def get_products_from_cache():
    """Функция возвращает данные из кэша или бд"""
    if not CACHE_ENABLED:
        return Product.objects.all()
    key = "product_list"
    products = cache.get(key)
    if products is not None:
        return products
    products = Product.objects.all()
    cache.set(key, products)
    return products