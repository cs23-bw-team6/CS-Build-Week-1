from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/adv/', include('adventure.urls')),
    path('', TemplateView.as_view(template_name='client/frontend/index.html')),
]
