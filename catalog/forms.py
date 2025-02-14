from django.core.exceptions import ValidationError
from django.forms import BooleanField, ModelForm

from catalog.models import Product

FORBIDDEN_WORDS = (
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
)
ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png"]


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class ProductForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "photo",
            "category",
            "price",
            "created_at",
            "updated_at",
        ]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        for word in FORBIDDEN_WORDS:
            if word in name.lower():
                raise ValidationError("Имя продукта не может содержать это слово")
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description")
        for word in FORBIDDEN_WORDS:
            if word in description.lower():
                raise ValidationError("Описание продукта не может содержать это слово")
        return description

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price < 0:
            raise ValidationError("Цена не может быть отрицательной")
        return price

    def clean_photo(self):
        max_size = 5 * 1024 * 1024
        photo = self.cleaned_data.get("photo")
        extension = photo.name.split(".")[-1].lower()
        if extension not in ALLOWED_EXTENSIONS:
            raise ValidationError("Неподходящий формат изображения")

        if photo.size > max_size:
            raise ValidationError(
                "Максимальный размер изображения не должен быть больше 5Мб"
            )

        return photo
