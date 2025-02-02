from django.db import models


class MyBlog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Описание')
    content = models.TextField(max_length=150)
    preview = models.ImageField(upload_to="../static/images")
    created_at = models.DateField(auto_now_add=True)
    public_status = models.BooleanField(default=True)
    views = models.IntegerField(default=0)
