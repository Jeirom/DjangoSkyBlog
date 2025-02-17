from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, View)

from catalog.forms import ProductForm
from catalog.models import Contact, Product


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

    def form_valid(self, form):
        form.instance.owner = self.request.user  # устанавливаем владельца продукта
        return super().form_valid(form)


class ProductListView(LoginRequiredMixin, ListView):
    """
    Контроллер для отображения списка продуктов.

    Требует, чтобы пользователь был аутентифицирован.
    """
    model = Product
    login_url = reverse_lazy('users:login')


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