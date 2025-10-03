from django.urls import path

from . import views

app_name = 'obras'

urlpatterns = [
    path('', views.obra_list, name='list'),
    path('nova/', views.obra_create, name='create'),
    path('<int:pk>/editar/', views.obra_update, name='update'),
    path('<int:pk>/excluir/', views.obra_delete, name='delete'),
    path('exportar/pdf/', views.obra_export_pdf, name='export_pdf'),
    path('exportar/excel/', views.obra_export_excel, name='export_excel'),
]
