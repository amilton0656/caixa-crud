from django.contrib import admin

from .models import CentroCusto


@admin.register(CentroCusto)
class CentroCustoAdmin(admin.ModelAdmin):
    list_display = ('id', 'descricao')
    search_fields = ('descricao',)
