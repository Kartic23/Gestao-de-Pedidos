from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from anoletivo.models import *
from main.models import *


class TipoDePedido(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'tipo_de_pedido'


class IdentificadorPedido(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='nome', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'identificador_pedido'

class EstadoPedido(models.Model):
    estado = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estado_pedido'



class Pedido(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    docenteutilizadorid = models.ForeignKey(Docente, models.DO_NOTHING, db_column='DocenteUtilizadorID')  # Field name made lowercase.
    funcionarioutilizadorid = models.ForeignKey(Funcionario, models.DO_NOTHING, db_column='FuncionarioUtilizadorID')  # Field name made lowercase.
    data_de_submissao = models.DateField(blank=True, null=True)
    data_de_associacao = models.DateTimeField(blank=True, null=True)
    data_de_validacao = models.DateTimeField(blank=True, null=True)
    identificador_id = models.ForeignKey(IdentificadorPedido,models.DO_NOTHING, db_column='identificador_id')
    anoletivoid = models.ForeignKey(ano_letivo, models.DO_NOTHING, db_column='anoletivoid')
    estado_0 = models.ForeignKey(EstadoPedido, models.DO_NOTHING, db_column='estado_id')  # Field renamed because of name conflict.
    tipo = models.ForeignKey('TipoDePedido', models.DO_NOTHING)
    data_de_alvo = models.DateField(blank=True, null=True)
    assunto = models.CharField(db_column='assunto', max_length=255, blank=True, null=True)  # Field name made lowercase.
    informacoes = models.CharField(db_column='informacoes', max_length=255, blank=True, null=True)  # Field name made lowercase.
    comentarios = models.CharField(db_column='comentarios', max_length=255, blank=True, null=True)  # Field name made lowercase.
    

    class Meta:
        managed = False
        db_table = 'pedido'



class PedidoOutros(Pedido):

    class Meta:
        #managed = False
        db_table = 'pedido_outros'


class Outros(models.Model):
    ID = models.AutoField(primary_key=True)
    Assunto = models.CharField(max_length=255)
    Descricao = models.CharField(max_length=500)
    pedido_ptr = models.ForeignKey(PedidoOutros, on_delete=models.CASCADE)

    class Meta:
        db_table = 'outros'



class PedidoDeHorario(Pedido):

    class Meta:
        managed = False
        db_table = 'pedido_de_horario'


class Horario(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    acao = models.CharField(max_length=255)
    data_h = models.DateField(blank=True,null=True)
    hora_inicial = models.TimeField(blank=True, null=True)
    hora_final = models.TimeField(blank=True, null=True)
    descricao = models.CharField(max_length=255)
    antigodata_h = models.DateField(blank=True,null=True)
    antigohora_inicial = models.TimeField(blank=True, null=True)
    antigohora_final = models.TimeField(blank=True, null=True)
    antigodescricao = models.CharField(max_length=255)
    pedido_ptr = models.ForeignKey(PedidoDeHorario, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'horario'
























class PedidoUc(Pedido):

    class Meta:
        # managed = False
        db_table = 'pedido_uc'



class Uc(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    period = models.CharField(db_column='Period', max_length=255, blank=True, null=True)  # Field name made lowercase.
    codigo = models.IntegerField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    disciplina = models.CharField(db_column='Disciplina', max_length=255, blank=True, null=True)  # Field name made lowercase.
    inst_discip = models.CharField(db_column='Inst_discip', max_length=255, blank=True, null=True)  # Field name made lowercase.
    inst_disciplina_full = models.CharField(db_column='Inst_disciplina_full', max_length=255, blank=True, null=True)  # Field name made lowercase.
    depart_disciplina = models.CharField(db_column='Depart_disciplina', max_length=255, blank=True, null=True)  # Field name made lowercase.
    turma = models.CharField(db_column='Turma', max_length=255, blank=True, null=True)  # Field name made lowercase.
    codigo_curso = models.IntegerField(db_column='Codigo_curso', blank=True, null=True)  # Field name made lowercase.
    curso = models.CharField(db_column='Curso', max_length=255, blank=True, null=True)  # Field name made lowercase.
    horas_semanais = models.IntegerField(blank=True, null=True)
    horas_periodo = models.IntegerField(blank=True, null=True)
    horas_servico = models.IntegerField(blank=True, null=True)
    data_inicio = models.DateField(blank=True, null=True)
    data_fim = models.DateField(blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'uc'


class DocenteUc(models.Model):
    docenteutilizadorid = models.OneToOneField(Docente, models.DO_NOTHING, db_column='DocenteUtilizadorID', primary_key=True)  # Field name made lowercase.
    ucid = models.ForeignKey('Uc', models.DO_NOTHING, db_column='UCID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'docente_uc'

class SubpedidoUc(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    ucid = models.CharField(db_column='ucid', max_length=255)
    descricao = models.CharField(db_column='descricao', max_length=255)
    acao = models.CharField(db_column='acao', max_length=255)
    turma = models.CharField(db_column='turma',max_length=255)
    pedido_ptr = models.ForeignKey(PedidoDeHorario, on_delete=models.CASCADE)

    class Meta:
        db_table = 'subpedido_uc'




class EstadoSala(models.Model):
    id =  models.AutoField(db_column='ID', primary_key=True)
    estado = models.CharField(db_column='estado', max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estado_sala'

class Acao(models.Model):
    id =  models.AutoField(db_column='ID', primary_key=True)
    acao = models.CharField(db_column='Name', max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acao'


class Categoria(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    tipo_de_sala = models.CharField(db_column='Name', max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categoria'

class Edificio(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    edificio = models.CharField(db_column='Name', max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'edificio'

class Instituicao(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    nome_instituicao = models.CharField(db_column='Name', max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instituicao'

class TipoDeAulas(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    tipo_aula = models.CharField(db_column='Name', max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipo_de_aulas'


class Sala(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)  # Field name made lowercase.
    id_estado_da_sala = models.CharField(db_column='Estado_Sala_id', max_length=255, blank=True, null=True)
    id_nome_instituicao = models.CharField(db_column='Nome_Instituicao_id', max_length=255, blank=True, null=True)  
    id_nome_edificio = models.CharField(db_column='Desc_Edificio_id', max_length=255, blank=True, null=True)
    id_nome_tipo_sala = models.CharField(db_column='Des_Categoria_id', max_length=255, blank=True, null=True)
    id_tipo_aula = models.CharField(db_column='Tipo_sala_id', max_length=255, blank=True, null=True)
    id_ano_letivo = models.CharField(db_column='ano_letivo_id', max_length=255, blank=True, null=True)
    descricao_sala = models.CharField(db_column='Desc_Sala', max_length=255, blank=True, null=True)
    lotacao = models.CharField(db_column='Lotacao_Presencial_Sala', max_length=255, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'sala'



class PedidoDeSala(Pedido):

    class Meta:
        #managed = False
        db_table = 'pedido_de_sala'


class subpedido_sala(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  
    descricao = models.CharField(db_column='descricao', max_length=255, blank=True, null=True)
    inicio = models.DateTimeField(db_column='inicio')
    fim = models.DateTimeField(db_column='fim')
    id_instituicao = models.CharField(db_column='Instituicao_id', max_length=255, blank=True, null=True)
    id_edificio =  models.CharField(db_column='Edificio_id', max_length=255, blank=True, null=True)
    id_sala =  models.CharField(db_column='Sala_id', max_length=255, blank=True, null=True)
    id_tipo_de_aula =  models.CharField(db_column='Tipo_de_aula_id', max_length=255, blank=True, null=True)
    categoria =  models.CharField(db_column='categoria', max_length=255, blank=True, null=True)
    numero_alunos =  models.CharField(db_column='Numero_Alunos', max_length=255, blank=True, null=True)
    acao = models.CharField(db_column='Acao', max_length=255, blank=True, null=True)
    pedido_ptr = models.ForeignKey(PedidoDeSala, on_delete=models.CASCADE)
    editar_inicio = models.DateTimeField(db_column='nova_inicio')
    editar_descricao = models.CharField(db_column='nova_descricao', max_length=255, blank=True, null=True)
    editar_fim = models.DateTimeField(db_column='nova_fim')
    editar_id_instituicao = models.CharField(db_column='nova_Instituicao_id', max_length=255, blank=True, null=True)
    editar_id_edificio =  models.CharField(db_column='nova_Edificio_id', max_length=255, blank=True, null=True)
    editar_id_sala =  models.CharField(db_column='nova_Sala_id', max_length=255, blank=True, null=True)
    editar_id_tipo_de_aula =  models.CharField(db_column='nova_Tipo_de_aula_id', max_length=255, blank=True, null=True)
    editar_categoria =  models.CharField(db_column='nova_categoria', max_length=255, blank=True, null=True)
    editar_numero_alunos =  models.CharField(db_column='nova_Numero_Alunos', max_length=255, blank=True, null=True)



    class Meta:
        managed = False
        db_table = 'subpedido_sala'

