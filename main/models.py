from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'



class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'



class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'

class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)

class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'




class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)

class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)

class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)




class Utilizador(User):

    class Meta:
        managed = False
        db_table = 'utilizador'


class Faculdade(models.Model):
    nome = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'faculdade'





class Departamento(models.Model):
    nome = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'departamento'

class Gabinete(models.Model):
    nome = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'gabinete'

class Docente(Utilizador):
    faculdadeid = models.ForeignKey('Faculdade', models.DO_NOTHING, db_column='Faculdadeid')  # Field name made lowercase.
    departamentoid = models.ForeignKey(Departamento, models.DO_NOTHING, db_column='Departamentoid')  # Field name made lowercase.
    gabineteid = models.ForeignKey('Gabinete', models.DO_NOTHING, db_column='Gabineteid')  # Field name made lowercase.
    ano_letivoid = models.IntegerField(db_column='ano_letivoid', blank=True, null=True)
    codigo = models.IntegerField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    ativo = models.CharField(db_column='Ativo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    individuo = models.IntegerField(db_column='Individuo', blank=True, null=True)  # Field name made lowercase.
    data_de_nascimento = models.DateField(db_column='Data_de_nascimento', blank=True, null=True)  # Field name made lowercase.
    sexo = models.CharField(db_column='Sexo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tipo_de_identificacao = models.IntegerField(db_column='Tipo_de_identificacao', blank=True, null=True)  # Field name made lowercase.
    identificacao = models.CharField(db_column='Identificacao', max_length=255, blank=True, null=True)  # Field name made lowercase.
    data_de_emissao_de_identificacao = models.DateField(db_column='Data_de_emissao_de_identificacao', blank=True, null=True)  # Field name made lowercase.
    nacionalidade = models.IntegerField(db_column='Nacionalidade', blank=True, null=True)  # Field name made lowercase.
    arquivo = models.IntegerField(db_column='Arquivo', blank=True, null=True)  # Field name made lowercase.
    data_de_validade_de_identificacao = models.DateField(db_column='Data_de_validade_de_identificacao', blank=True, null=True)  # Field name made lowercase.
    nif = models.IntegerField(db_column='Nif', blank=True, null=True)  # Field name made lowercase.
    pais_fiscal = models.IntegerField(db_column='Pais_fiscal', blank=True, null=True)  # Field name made lowercase.
    digito_verificacao = models.IntegerField(db_column='Digito_verificacao', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'docente'

class Funcionario(Utilizador):

    class Meta:
        #managed = False
        db_table = 'funcionario'

class PCP(Utilizador):

    class Meta:
        #managed = False
        db_table = 'pcp'