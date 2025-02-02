from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sky_blog.urls'), name='myblog'),
    path('catalog/', include('catalog.urls'), name='catalog'),
]
