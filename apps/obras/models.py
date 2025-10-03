from django.db import models


class Obra(models.Model):
    nome = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    municipio = models.CharField(max_length=100)

    class Meta:
        db_table = 'obras'
        ordering = ['nome']
        verbose_name = 'Obra'
        verbose_name_plural = 'Obras'

    def __str__(self) -> str:
        return self.nome
