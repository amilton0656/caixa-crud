from django.urls import path

from . import views

app_name = 'caixa'

urlpatterns = [
    path('', views.movimento_list, name='movimento_list'),
    path('novo/', views.movimento_create, name='movimento_create'),
    path('<int:pk>/editar/', views.movimento_update, name='movimento_update'),
    path('<int:pk>/excluir/', views.movimento_delete, name='movimento_delete'),
    path('exportar/pdf/', views.movimento_export_pdf, name='export_pdf'),
    path('exportar/excel/', views.movimento_export_excel, name='export_excel'),
]
