from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import Group
from .forms import LoginForm
from django.shortcuts import render
from django.views.generic.list import *
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import *
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import F
import datetime
from dateutil import parser
from django.core.exceptions import ObjectDoesNotExist
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.http import HttpResponse
from django.http import FileResponse
import csv
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView



def homepage(request):
    return render(request,"inicio.html")

def escolher_perfil(request):
    ''' Escolher tipo de perfil para criar um utilizador '''
    u=""
    utilizadores = ["Funcionário","Docente"]
    return render(request, 
                  template_name='escolher_perfil.html',
                  context={"utilizadores": utilizadores,'u': u})

def criar_utilizador(request, id): 
    tipo = id
    form = ""
    u = ""
    msg = False    
    perfil = ""
    if request.method == "POST":
        if tipo == 1:
            form = FuncionarioRegisterForm(request.POST)
            perfil = "Funcionario"
            my_group = Group.objects.get(name='Funcionario') 
        elif tipo == 2:
            form = DocenteRegisterForm(request.POST)
            perfil = "Docente"
            my_group = Group.objects.get(name='Docente')
        if form.is_valid():
            user = form.save()
            my_group.user_set.add(user)
            if tipo == 1:
                user.valido = 'True'
                user.save()
            elif tipo == 2:
                user.valido = 'True'
                user.save()

            return redirect("main:concluir-registo-utilizador",1)
        else:
            msg=True
            tipo = id
            return render(request=request,
                              template_name="criar_utilizador.html",
                              context={"form": form, 'perfil': perfil, 'u': u,'registo' : tipo,'msg': msg})
    else:
        if tipo == 1:
            form = FuncionarioRegisterForm()
            perfil = "Funcionario"
        elif tipo == 2:
            form = DocenteRegisterForm()
            perfil = "Docente"

        return render(request=request,
                  template_name="criar_utilizador.html",
                  context={"form": form, 'perfil': perfil,'u': u,'registo' : tipo,'msg': msg})
            
def concluir_registo_utilizador(request,id):
    ''' Página que é mostrada ao utilizador quando faz um registo na plataforma '''
    return render(request=request,
                  template_name="concluir_registo_utilizador.html",
                  context={'participante': id})


###########################################
#Pagina relacionadas com o login e logout #
###########################################
def login_action(request):
    ''' Fazer login na plataforma do dia aberto e gestão de acessos à plataforma '''
    u=""
    msg=False
    error=""
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username=="" or password=="":
                msg=True
                error="Todos os campos são obrigatórios!"
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main:mensagem',1)
            else:
                msg=True
                error="O nome de utilizador ou a palavra-passe inválidos!"
    form = LoginForm()
    return render(request,
                  template_name="login.html",
                  context={"form": form,"msg": msg, "error": error})


def logout_action(request):
    ''' Fazer logout na plataforma '''
    logout(request)
    return redirect('main:mensagem',2)



##################################################
#Pagina relacionadas com a exposição da mensagem #
##################################################
def mensagem(request, id):
    ''' Template de mensagens informativas/erro/sucesso '''
    user = get_user(request)
    if id == 400 or id == 500:
        m = "Erro no servidor"
        tipo = "error"
    elif id == 1:
        m = "Bem vindo(a) " + user.first_name 
        tipo = "info"
    elif id == 2:
        m = "Até á próxima!"
        tipo = "info"
    elif id == 3:
        m = "Registo feito com sucesso!"
        tipo = "sucess"
    elif id == 4:
        m = "Pedido criado com sucesso"
        tipo = "success"
    elif id == 5:
        m = "Pedido Alterado com sucesso"
        tipo = "success"
    elif id == 6:
        m = "Pedido eliminado com sucesso!"
        tipo = "success"    
    elif id == 7:
        m = "Pedido não pode ser eliminado pois não está no estado 'Pendente'"
        tipo = "error"   
    elif id == 8:
        m = "Funcionarios não podem eliminar pedidos"
        tipo = "info" 
    elif id == 9:
        m = "Ano Letivo criado com sucesso"
        tipo = "success" 
    elif id == 10:
        m = "Ano Letivo Eliminado com sucesso"
        tipo = "success"
    elif id == 12:
        m = "Pedido associado a Funcionario com sucesso"
        tipo = "success"
    elif id == 11:
        m = "Ano Letivo ativado com Sucesso"
        tipo = "success"
    elif id == 13:
        m = "Este ano letivo não pode ser ativado."
        tipo = "error" 
    elif id == 14:
        m = "Não existem mensagens"
        tipo = "info"  
    elif id == 15:
        m = "Pedido Validado com sucesso"
        tipo = "success"  
    elif id == 16:
        m = "Este ano letivo têm pedidos associados , assim ainda não se pode eliminar "
        tipo = "info"                 
    elif id == 17:
        m = "A sua disponibilidade foi alterada com sucesso"
        tipo = "success"
    elif id == 18:
        m = "Antes de poder ver dados e estatísticas é preciso configurar um Dia Aberto."
        tipo = "error"
    elif id == 20:
        m = "Ficheiro têm de ser do tipo .xls"
        tipo = "error"
    elif id == 21:
        m = "Ficheiro têm de ter as seguintes colunas: Coluna Vazia | Ano letivo | Docente | Regência | Tipo"
        tipo = "error"
    elif id == 22:
        m = "Pedido desassociado a Funcionario com sucesso"
        tipo = "success"
    elif id == 23:
        m = "Ficheiro têm de ter as seguintes colunas: Codigo | Docente | Ativo | Nome | Individuo | Data Nascimento | Sexo | Tipo de Identificação | Identificação | Data de emisão da Identificação | Nacionalidade | Arquivo | Data de validade"
        tipo = "error"
    elif id == 25:
        m = "Email enviado ao PCP"
        tipo = "success"
    else:
        m = "Esta pagina não existe"
        tipo = "error"
    return render(request=request,
        template_name="mensagem.html", context={'m': m, 'tipo': tipo })
