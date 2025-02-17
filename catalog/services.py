from catalog.models import Product


def get_product_by_category(category_id):
    return Product.objects.filter(category=category_id)