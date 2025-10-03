from django.db import models
from django.utils import timezone

from apps.centros_custos.models import CentroCusto
from apps.obras.models import Obra


class Movimento(models.Model):
    ENTRADA = '+'
    SAIDA = '-'
    SINAL_CHOICES = [
        (ENTRADA, 'Entrada'),
        (SAIDA, 'Saida'),
    ]

    obra = models.ForeignKey(Obra, on_delete=models.PROTECT, related_name='movimentos')
    centro_custos = models.ForeignKey(CentroCusto, on_delete=models.PROTECT, related_name='movimentos')
    data = models.DateField(default=timezone.now)
    sinal = models.CharField(max_length=1, choices=SINAL_CHOICES)
    historico = models.TextField()

    class Meta:
        db_table = 'movimento'
        ordering = ['-data']
        verbose_name = 'Movimento'
        verbose_name_plural = 'Movimentos'

    def __str__(self) -> str:
        return f"{self.get_sinal_display()} - {self.obra} ({self.data:%d/%m/%Y})"
