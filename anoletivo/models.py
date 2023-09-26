from django.db import models

# Create your models here.
class ano_letivo(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    ano_letivo = models.CharField(db_column='ano_letivo', max_length=255)
    dia_inicio = models.DateField(blank=True, null=True)
    dia_fim = models.DateField(blank=True, null=True)
    ativo = models.CharField(db_column='ativo', max_length=10)

    class Meta:
        #managed = False
        db_table = 'ano_letivo'