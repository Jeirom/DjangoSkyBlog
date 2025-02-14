from sky_blog.models import MyBlog
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy


class SkyBlogListView(ListView):
    """Класс, показывающий список всех сущностей."""
    model = MyBlog
    fields = ['title','content']#, 'view', 'created_at', 'image', 'public_status']
    template_name = 'mymodel_list.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        return MyBlog.objects.filter(public_status=True).order_by('created_at')


class SkyBlogCreateView(CreateView):
    """А этот класс создает и добавляет в 'mymodel_list' блог."""
    model = MyBlog
    fields = ['title', 'content']
    template_name = 'mymodel_form.html'
    success_url = reverse_lazy('mymodel_list')


class SkyBlogDetailView(DetailView):
    """Этот класс показывает детальную информацию по блогу."""
    model = MyBlog
    template_name = 'mymodel_detail.html'
    context_object_name = 'mymodel'

    def get_object(self, queryset=None):
        """Счетчик просмотров"""
        obj = super().get_object()
        obj.views += 1 # +1 к переменной views за каждый CTRL + R
        obj.save()
        return obj


class SkyBlogUpdateView(UpdateView):
    """Этот обновляет информацию"""
    model = MyBlog
    fields = ['title','content']
    template_name = 'mymodel_edit.html'
    success_url = reverse_lazy('mymodel_list')

    def get_success_url(self):
        return reverse_lazy('mymodel_detail', args=[self.kwargs.get('pk')])

class SkyBlogDeleteView(DeleteView):
    """А этот удаляет блог"""
    model = MyBlog
    template_name = 'mymodel_confirm_delete.html'
    success_url = reverse_lazy('mymodel_list')