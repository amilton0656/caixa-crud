from django.contrib import admin

from .models import Movimento


@admin.register(Movimento)
class MovimentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'obra', 'centro_custos', 'data', 'sinal', 'valor')
    list_filter = ('sinal', 'data', 'obra', 'centro_custos')
    search_fields = ('historico',)
    date_hierarchy = 'data'
