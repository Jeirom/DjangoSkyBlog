from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, View)

from catalog.forms import ProductForm
from catalog.models import Contact, Product, Category
from catalog.services import get_products_by_category



class ContactsView(LoginRequiredMixin, View):
    """
    Контроллер для отображения страницы контактов.

    Требует, чтобы пользователь был аутентифицирован.
    """
    model = Contact
    login_url = reverse_lazy('users:login')

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Обрабатывает GET-запрос для отображения страницы контактов.

        :param request: HTTP-запрос.
        :return: Ответ с HTML-страницей контактов.
        """
        return render(request, "catalog/contacts.html")


class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Контроллер для создания нового продукта.

    Требует, чтобы пользователь был аутентифицирован.
    """
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")
    login_url = reverse_lazy('users:login')


class ProductsByCategoryView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "catalog/product_category.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.object.pk
        context["products"] = get_products_by_category(pk)
        return context


class ProductListView(LoginRequiredMixin, ListView):
    """
    Контроллер для отображения списка продуктов.

    Требует, чтобы пользователь был аутентифицирован.
    """
    model = Product
    login_url = reverse_lazy('users:login')

    @method_decorator(cache_page(60 * 15))
    def get_queryset(self):
        """
        Фильтруем продукты в зависимости от прав пользователя.
        """
        # Получаем продукты из кэша или базы данных
        queryset = get_products_from_cache()

        # Проверяем наличие прав can_unpublish_product у пользователя
        if self.request.user.has_perm('app_label.can_unpublish_product'):
            # Если права есть, возвращаем все продукты
            return queryset
        else:
            # Если прав нет, фильтруем прошедшие публикацию
            return queryset.filter(public_status=True)




class ProductDetailView(LoginRequiredMixin, DetailView):
    """
    Контроллер для отображения деталей конкретного продукта.

    Требует, чтобы пользователь был аутентифицирован.
    """
    model = Product
    login_url = reverse_lazy('users:login')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер для обновления существующего продукта.

    Требует, чтобы пользователь был аутентифицирован.
    """
    model = Product
    form_class = ProductForm
    login_url = reverse_lazy('users:login')

    def get_success_url(self) -> str:
        """
        Возвращает URL для перенаправления после успешного обновления продукта.

        :return: URL-адрес для перенаправления.
        """
        return reverse_lazy("catalog:product_detail", kwargs={"pk": self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner != request.user:
            return self.handle_no_permission()

        # Проверка разрешения can_unpublish_product
        if not request.user.has_perm('product.can_unpublish_product'):
            raise PermissionDenied("У вас нет прав для обновления этого продукта.")

        return super().dispatch(request, *args, **kwargs)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """
    Контроллер для удаления существующего продукта.

    Требует, чтобы пользователь был аутентифицирован.
    """
    model = Product
    success_url = reverse_lazy("catalog:product_list")
    login_url = reverse_lazy('users:login')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner != request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
