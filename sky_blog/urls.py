from django.urls import path

from sky_blog.views import SkyBlogListView, SkyBlogDeleteView, SkyBlogDetailView, SkyBlogUpdateView, SkyBlogCreateView

urlpatterns = [
    path('blog/', SkyBlogListView.as_view(), name='mymodel_list'), #Список всех блогов
    path('blog/<int:pk>/delete/', SkyBlogDeleteView.as_view(), name='mymodel_confirm_delete'), #Шаблон удаление блога
    path('blog/<int:pk>/', SkyBlogDetailView.as_view(), name='mymodel_detail'), #Шаблон с детальной инфой по блогам
    path('blog/<int:pk>/edit/',SkyBlogUpdateView.as_view(), name='mymodel_edit'), #Шаблон с обновлением информации
    path('blog/new/', SkyBlogCreateView.as_view(), name='mymodel_form'), #Создание новой сущности
]
