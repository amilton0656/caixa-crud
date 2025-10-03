from django.urls import path

from . import views

app_name = 'centros_custos'

urlpatterns = [
    path('', views.centrocusto_list, name='list'),
    path('novo/', views.centrocusto_create, name='create'),
    path('<int:pk>/editar/', views.centrocusto_update, name='update'),
    path('<int:pk>/excluir/', views.centrocusto_delete, name='delete'),
    path('exportar/pdf/', views.centrocusto_export_pdf, name='export_pdf'),
    path('exportar/excel/', views.centrocusto_export_excel, name='export_excel'),
]
