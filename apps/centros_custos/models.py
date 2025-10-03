from django.db import models


class CentroCusto(models.Model):
    descricao = models.CharField(max_length=255)

    class Meta:
        db_table = 'centros_custos'
        ordering = ['descricao']
        verbose_name = 'Centro de Custo'
        verbose_name_plural = 'Centros de Custo'

    def __str__(self) -> str:
        return self.descricao
