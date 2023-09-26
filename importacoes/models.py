from django.db import models
from main.models import *
from anoletivo.models import *

# Create your models here.

class Curso(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)  # Field name made lowercase.
    curso_nome = models.CharField(db_column='curso_nome', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ciclo = models.IntegerField(db_column='ciclo') 
    codigo = models.IntegerField(db_column='codigo') 

    class Meta:
        #managed = False
        db_table = 'curso'

class TipoDeRegencia(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='tipo', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'tipo_de_regencia'

class Regencia(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)  # Field name made lowercase.
    docente_id = models.ForeignKey(Docente, models.DO_NOTHING, db_column='docente_id')      
    ano_letivo_id = models.ForeignKey(ano_letivo, models.DO_NOTHING, db_column='ano_letivo_id')    
    regencia_id = models.IntegerField(db_column='regencia_id') 
    tipo_regencia_id = models.ForeignKey(TipoDeRegencia, models.DO_NOTHING, db_column='tipo_regencia_id')   

    class Meta:
        managed = False
        db_table = 'regencia'