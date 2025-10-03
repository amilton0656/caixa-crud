from django.contrib import admin
from django.urls import include, path

from apps.caixa.views import login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', include('apps.caixa.urls')),
    path('obras/', include('apps.obras.urls')),
    path('centros-de-custos/', include('apps.centros_custos.urls')),
]
