from django.contrib import admin

from .models import Obra


@admin.register(Obra)
class ObraAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'municipio')
    search_fields = ('nome', 'municipio')
