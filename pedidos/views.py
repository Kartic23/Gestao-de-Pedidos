from email.message import EmailMessage
import smtplib
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import Group
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
import json
import re
from .tables import PedidosTable
from .tables import ExportarPedidosTable
from .filters import PedidoFilter
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.http import HttpResponse
from django.http import FileResponse
import csv
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
import os
from django.conf import settings
from notificacoes.models import *




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
        tipo = "info"
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
        m = "Este ano letivo têm pedidos ainda pendentes , assim ainda não se pode eliminar "
        tipo = "info"                 
    elif id == 17:
        m = "A sua disponibilidade foi alterada com sucesso"
        tipo = "success"
    elif id == 18:
        m = "Antes de poder ver dados e estatísticas é preciso configurar um Dia Aberto."
        tipo = "error"
    else:
        m = "Esta pagina não existe"
        tipo = "error"
    return render(request=request,
        template_name="main/mensagem.html", context={'m': m, 'tipo': tipo })



def listar_pedidos(request):
    if request.user != None:
        user = get_user(request)
        if user.groups.filter(name = "Docente").exists():
            docente = Docente.objects.get(pk=request.user.id)   
            pedidos = Pedido.objects.filter(docenteutilizadorid=docente)
            pedidos_com_dados = []
            for pedido in pedidos:
                pedido = {
                    'id': pedido.id,
                    'assunto': pedido.assunto,
                    'data_de_submissao': pedido.data_de_submissao.strftime('%d/%m/%Y'),
                    'estado_0': EstadoPedido.objects.get(id=pedido.estado_0.id).estado,
                    'data_de_alvo': pedido.data_de_alvo.strftime('%d/%m/%Y'),
                    'descricao': pedido.informacoes,
                    'tipo_Pedido':TipoDePedido.objects.get(id=pedido.tipo.id).tipo,
                }
                pedidos_com_dados.append(pedido)
                    
            return render(request, 
                        'pedido/listar_pedidos.html', 
                        context={'pedidos': pedidos_com_dados})
        elif user.groups.filter(name = "Funcionario").exists():
            pedidos = Pedido.objects.all()
            pedidos_com_dados = []
            for pedido in pedidos:
                if(pedido.estado_0.id == 1):
                    pedido = {
                        'id': pedido.id,
                        'assunto': pedido.assunto,
                        'data_de_submissao': pedido.data_de_submissao.strftime('%d/%m/%Y'),
                        'estado_0': EstadoPedido.objects.get(id=pedido.estado_0.id).estado,
                        'data_de_alvo': pedido.data_de_alvo.strftime('%d/%m/%Y'),
                        'descricao': pedido.informacoes,
                        'tipo_Pedido':TipoDePedido.objects.get(id=pedido.tipo.id).tipo,
                        'id_funcionario': ""
                    }
                else:
                    pedido = {
                        'id': pedido.id,
                        'assunto': pedido.assunto,
                        'data_de_submissao': pedido.data_de_submissao.strftime('%d/%m/%Y'),
                        'estado_0': EstadoPedido.objects.get(id=pedido.estado_0.id).estado,
                        'data_de_alvo': pedido.data_de_alvo.strftime('%d/%m/%Y'),
                        'descricao': pedido.informacoes,
                        'tipo_Pedido':TipoDePedido.objects.get(id=pedido.tipo.id).tipo,
                        'id_funcionario': pedido.funcionarioutilizadorid
                    }
                    
                pedidos_com_dados.append(pedido)
            return render(request, 
                        'pedido/listar_pedidos.html', 
                        context={'pedidos': pedidos_com_dados})

    else:
        return redirect('main:mensagem',222)
    

class exportar_pedidos_table(SingleTableMixin, FilterView):
    ''' Consultar todos os pedidos com as funcionalidades dos filtros '''
    table_class = ExportarPedidosTable
    template_name = "pedido/exportar_pedidos.html"
    filterset_class = PedidoFilter
    table_pagination ={
        'per_page': 10
    }

    
    def get_queryset(self):
        queryset = Pedido.objects.all()
        if self.request.user.groups.filter(name='Docente').exists():
            queryset = queryset.filter(docenteutilizadorid=self.request.user.id)

        return queryset
        
    def get_context_data(self, **kwargs):
        context = super(SingleTableMixin, self).get_context_data(**kwargs)
        table = self.get_table(**self.get_table_kwargs())
        table.request = self.request
        table.fixed = True
        context[self.get_context_table_name(table)] = table
        return context


class consultar_pedidos(SingleTableMixin, FilterView):
    ''' Consultar todos os pedidos com as funcionalidades dos filtros '''
    table_class = PedidosTable
    template_name = "pedido/listagem_pedidos.html"
    filterset_class = PedidoFilter
    table_pagination ={
        'per_page': 10
    }

    
    def get_queryset(self):
        queryset = Pedido.objects.filter(anoletivoid=ano_letivo.objects.get(ativo="S")).all()
        if self.request.user.groups.filter(name='Docente').exists():
            queryset = queryset.filter(docenteutilizadorid=self.request.user.id)

        return queryset
        
    def get_context_data(self, **kwargs):
        context = super(SingleTableMixin, self).get_context_data(**kwargs)
        table = self.get_table(**self.get_table_kwargs())
        table.request = self.request
        table.fixed = True
        context[self.get_context_table_name(table)] = table
        return context

def exportar_pedidos(request):
    if request.user != None:
        user = get_user(request)
        if request.method == 'POST':
            tipohorario = request.POST.get('horario')
            tipooutros = request.POST.get('outros')
            tiposala = request.POST.get('sala')
            tipouc = request.POST.get('uc')
            data_inicio = request.POST.get('data_de_inicio')
            data_fim = request.POST.get('data_de_fim')
            if user.groups.filter(name = "Docente").exists():
                docente = Docente.objects.get(pk=request.user.id)
                pedidos = Pedido.objects.filter(docenteutilizadorid=docente, anoletivoid=ano_letivo.objects.get(ativo="S"))
                if data_inicio == "":
                    if tipohorario == 'horario':
                        pedidos = Pedido.objects.filter(docenteutilizadorid=docente, tipo_id="1", anoletivoid=ano_letivo.objects.get(ativo="S"))
                        response = exportar_todos_pedidos_filtros_csv(pedidos)
                    elif tipooutros == 'outros':
                        pedidos = Pedido.objects.filter(docenteutilizadorid=docente, tipo_id="2", anoletivoid=ano_letivo.objects.get(ativo="S"))
                        response = exportar_todos_pedidos_filtros_csv(pedidos)
                    elif tiposala == 'sala':
                        pedidos = Pedido.objects.filter(docenteutilizadorid=docente, tipo_id="3", anoletivoid=ano_letivo.objects.get(ativo="S"))
                        response = exportar_todos_pedidos_filtros_csv(pedidos)
                    elif tipouc == 'uc':
                        pedidos = Pedido.objects.filter(docenteutilizadorid=docente, tipo_id="4", anoletivoid=ano_letivo.objects.get(ativo="S"))
                        response = exportar_todos_pedidos_filtros_csv(pedidos)
                    else:
                        pedidos = Pedido.objects.filter(docenteutilizadorid=docente, anoletivoid=ano_letivo.objects.get(ativo="S"))
                        response = exportar_todos_pedidos_filtros_csv(pedidos)
                elif data_inicio != "" and data_fim != "":
                    if tipohorario == 'horario':
                        pedidos = Pedido.objects.filter(data_de_submissao__range=(data_inicio, data_fim), docenteutilizadorid=docente, tipo_id="1", anoletivoid=ano_letivo.objects.get(ativo="S"))
                        response = exportar_todos_pedidos_filtros_csv(pedidos)
                    elif tipooutros == 'outros':
                        pedidos = Pedido.objects.filter(data_de_submissao__range=(data_inicio, data_fim), docenteutilizadorid=docente, tipo_id="2", anoletivoid=ano_letivo.objects.get(ativo="S"))
                        response = exportar_todos_pedidos_filtros_csv(pedidos)
                    elif tiposala == 'sala':
                        pedidos = Pedido.objects.filter(data_de_submissao__range=(data_inicio, data_fim), docenteutilizadorid=docente, tipo_id="3", anoletivoid=ano_letivo.objects.get(ativo="S"))
                        response = exportar_todos_pedidos_filtros_csv(pedidos)
                    elif tipouc == 'uc':
                        pedidos = Pedido.objects.filter(data_de_submissao__range=(data_inicio, data_fim), docenteutilizadorid=docente, tipo_id="4", anoletivoid=ano_letivo.objects.get(ativo="S"))
                        response = exportar_todos_pedidos_filtros_csv(pedidos)
                    else:
                        pedidos = Pedido.objects.filter(data_de_submissao__range=(data_inicio, data_fim), docenteutilizadorid=docente, anoletivoid=ano_letivo.objects.get(ativo="S"))
                        response = exportar_todos_pedidos_filtros_csv(pedidos)
                pedidos_com_dados = []
                for pedido in pedidos:
                    pedido = {
                        'id': pedido.id,
                        'assunto': pedido.assunto,
                        'data_de_submissao': pedido.data_de_submissao.strftime('%d/%m/%Y'),
                        'estado_0': EstadoPedido.objects.get(id=pedido.estado_0.id).estado,
                        'data_de_alvo': pedido.data_de_alvo.strftime('%d/%m/%Y'),
                        'descricao': pedido.informacoes,
                        'tipo_Pedido':TipoDePedido.objects.get(id=pedido.tipo.id).tipo,
                    }
                    pedidos_com_dados.append(pedido)
                return response
            
            elif user.groups.filter(name = "Funcionario").exists():
                pedidos = Pedido.objects.all()
                if data_inicio == "":
                    if tipohorario == 'horario':
                        pedidos = Pedido.objects.filter(tipo_id="1", anoletivoid=ano_letivo.objects.get(ativo="S"))
                        response = exportar_todos_pedidos_filtros_csv(pedidos)
                    elif tipooutros == 'outros':
                        pedidos = Pedido.objects.filter(tipo_id="2", anoletivoid=ano_letivo.objects.get(ativo="S"))
                        response = exportar_todos_pedidos_filtros_csv(pedidos)
                    elif tiposala == 'sala':
                        pedidos = Pedido.objects.filter(tipo_id="3", anoletivoid=ano_letivo.objects.get(ativo="S"))
                        response = exportar_todos_pedidos_filtros_csv(pedidos)
                    elif tipouc == 'uc':
                        pedidos = Pedido.objects.filter(tipo_id="4", anoletivoid=ano_letivo.objects.get(ativo="S"))
                        response = exportar_todos_pedidos_filtros_csv(pedidos)
                    else:
                        pedidos = Pedido.objects.filter(anoletivoid=ano_letivo.objects.get(ativo="S"))
                        response = exportar_todos_pedidos_filtros_csv(pedidos)

                elif data_inicio != "" and data_fim != "":
                    if tipohorario == 'horario':
                        pedidos = Pedido.objects.filter(data_de_submissao__range=(data_inicio, data_fim), tipo_id="1", anoletivoid=ano_letivo.objects.get(ativo="S"))
                        response = exportar_todos_pedidos_filtros_csv(pedidos)
                    elif tipooutros == 'outros':
                        pedidos = Pedido.objects.filter(data_de_submissao__range=(data_inicio, data_fim), tipo_id="2", anoletivoid=ano_letivo.objects.get(ativo="S"))
                        response = exportar_todos_pedidos_filtros_csv(pedidos)
                    elif tiposala == 'sala':
                        pedidos = Pedido.objects.filter(data_de_submissao__range=(data_inicio, data_fim), tipo_id="3", anoletivoid=ano_letivo.objects.get(ativo="S"))
                        response = exportar_todos_pedidos_filtros_csv(pedidos)
                    elif tipouc == 'uc':
                        pedidos = Pedido.objects.filter(data_de_submissao__range=(data_inicio, data_fim), tipo_id="4", anoletivoid=ano_letivo.objects.get(ativo="S"))
                        response = exportar_todos_pedidos_filtros_csv(pedidos)
                    else:
                        pedidos = Pedido.objects.filter(data_de_submissao__range=(data_inicio, data_fim), anoletivoid=ano_letivo.objects.get(ativo="S"))
                        response = exportar_todos_pedidos_filtros_csv(pedidos)
                pedidos = Pedido.objects.all()
                pedidos_com_dados = []
                for pedido in pedidos:
                    pedido = {
                        'id': pedido.id,
                        'assunto': pedido.assunto,
                        'data_de_submissao': pedido.data_de_submissao.strftime('%d/%m/%Y'),
                        'estado_0': EstadoPedido.objects.get(id=pedido.estado_0.id).estado,
                        'data_de_alvo': pedido.data_de_alvo.strftime('%d/%m/%Y'),
                        'descricao': pedido.informacoes,
                        'tipo_Pedido':TipoDePedido.objects.get(id=pedido.tipo.id).tipo,
                    }
                    pedidos_com_dados.append(pedido)
                return response
        else:
            pedidos = Pedido.objects.all()
            response = exportar_todos_pedidos_filtros_csv(pedidos)
            pedidos_com_dados = []
            for pedido in pedidos:
                pedido = {
                    'id': pedido.id,
                    'assunto': pedido.assunto,
                    'data_de_submissao': pedido.data_de_submissao.strftime('%d/%m/%Y'),
                    'estado_0': EstadoPedido.objects.get(id=pedido.estado_0.id).estado,
                    'data_de_alvo': pedido.data_de_alvo.strftime('%d/%m/%Y'),
                    'descricao': pedido.informacoes,
                    'tipo_Pedido':TipoDePedido.objects.get(id=pedido.tipo.id).tipo,
                }
                pedidos_com_dados.append(pedido)
            return render(request, 
                        'pedido/exportar_pedidos.html', 
                        context={'pedidos': pedidos_com_dados})


    else:
        return redirect('main:mensagem',222)



def exportar_todos_pedidos_filtros_csv(pedido):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=pedidos.csv'
    writer = csv.writer(response)
    for pedidos in pedido:
        writer.writerow(['Assunto', 'Data Alvo', 'Descricao', 'Tipo de Pedido'])
        if (str(pedidos.tipo) == "TipoDePedido object (1)"):
            writer.writerow([pedidos.assunto, pedidos.data_de_alvo, pedidos.informacoes, 'Horario'])
            horario = Horario.objects.filter(pedido_ptr_id=pedidos.id)
            writer.writerow(['Data Horario', 'Hora inicial', 'Hora final', 'Descricao'])
            for horarios in horario:
                writer.writerow([horarios.data_h, horarios.hora_inicial, horarios.hora_final, horarios.descricao])
        elif(str(pedidos.tipo) == "TipoDePedido object (2)"):
            writer.writerow([pedidos.assunto, pedidos.data_de_alvo, pedidos.informacoes, 'Outros'])
            outros = Outros.objects.filter(pedido_ptr_id=pedidos.id)
            writer.writerow(['Assunto', 'Descrição'])
            for outro in outros:
                writer.writerow([outro.Assunto, outro.Descricao])
        elif(str(pedidos.tipo) == "TipoDePedido object (3)"):
            writer.writerow([pedidos.assunto, pedidos.data_de_alvo, pedidos.informacoes, 'Sala'])
            salas = subpedido_sala.objects.filter(pedido_ptr_id=pedidos.id)
            for sala in salas:
                if sala.acao == 3 and sala.numero_alunos is None:
                    writer.writerow(['Descricao', 'inicio', 'fim', 'acao', 'Sala Especifica', 'Numero de alunos' ])
                    writer.writerow([sala.editar_descricao, sala.editar_inicio, sala.editar_fim, Acao.objects.get(id=sala.acao).acao, Sala.objects.get(id=sala.editar_id_sala).descricao_sala, "0"])
                elif(sala.acao == 3):
                    writer.writerow(['Descricao', 'inicio', 'fim', 'instituicao', 'edificio','numero de alunos', 'acao'])
                    writer.writerow([sala.editar_descricao, sala.editar_inicio,sala.editar_fim, Instituicao.objects.get(id = sala.editar_id_instituicao).nome_instituicao, Edificio.objects.get(id=sala.editar_id_edificio).edificio, sala.editar_numero_alunos, Acao.objects.get(id=sala.acao).acao])
                elif(sala.numero_alunos is None):
                    writer.writerow(['Descricao', 'inicio', 'fim', 'acao', 'sala especifica', 'Numero de alunos'])
                    writer.writerow([sala.descricao, sala.inicio, sala.fim, Acao.objects.get(id=sala.acao).acao, Sala.objects.get(id=sala.id_sala).descricao_sala, "0"])
                else:
                    writer.writerow(['Descricao', 'inicio', 'fim', 'instituicao', 'edificio', 'numero de alunos', 'acao'])
                    writer.writerow([sala.descricao, sala.inicio, sala.fim, Instituicao.objects.get(id = sala.id_instituicao).nome_instituicao, Edificio.objects.get(id=sala.id_edificio).edificio, sala.numero_alunos, Acao.objects.get(id=sala.acao).acao])
        elif(str(pedidos.tipo) == "TipoDePedido object (4)"):
            writer.writerow([pedidos.assunto, pedidos.data_de_alvo, pedidos.informacoes, 'Unidade Curricular'])
            uc = SubpedidoUc.objects.filter(pedido_ptr_id=pedidos.id)
            writer.writerow(['Acao','Unidade Curricular', 'Turma', 'Descricao'])
            for ucs in uc:
                writer.writerow([ucs.acao, Uc.objects.get(id=ucs.ucid).disciplina, ucs.turma, ucs.descricao])
        writer.writerow([])


    return response



def exportar_pedidos_csv(request,id):
    response = HttpResponse(content_type='text/csv')
    pedidos = Pedido.objects.get(id=id) 
    response['Content-Disposition'] = 'attachment; filename=pedido'+pedidos.assunto+'.csv'
    writer = csv.writer(response)

    writer.writerow(['Assunto', 'Data Alvo', 'Descricao', 'Tipo de Pedido'])
    if (str(pedidos.tipo) == "TipoDePedido object (1)"):
        writer.writerow([pedidos.assunto, pedidos.data_de_alvo, pedidos.informacoes, 'Horario'])
        horario = Horario.objects.filter(pedido_ptr_id=pedidos.id)
        writer.writerow(['Acao', 'Data Horario', 'Hora inicial', 'Hora final', 'Descricao'])
        for horarios in horario:
            if(horarios.acao == "alterar"):
                writer.writerow([horarios.acao, horarios.antigodata_h, horarios.antigohora_inicial, horarios.antigohora_final, horarios.antigodescricao])
                writer.writerow([horarios.acao, horarios.data_h, horarios.hora_inicial, horarios.hora_final, horarios.descricao])
            else:
                writer.writerow([horarios.acao, horarios.data_h, horarios.hora_inicial, horarios.hora_final, horarios.descricao])
    elif(str(pedidos.tipo) == "TipoDePedido object (2)"):
        writer.writerow([pedidos.assunto, pedidos.data_de_alvo, pedidos.informacoes, 'Outros'])
        outros = Outros.objects.filter(pedido_ptr_id=pedidos.id)
        writer.writerow(['Assunto', 'Descrição'])
        for outro in outros:
            writer.writerow([outro.Assunto, outro.Descricao])
    elif(str(pedidos.tipo) == "TipoDePedido object (3)"):
        writer.writerow([pedidos.assunto, pedidos.data_de_alvo, pedidos.informacoes, 'Sala'])
        salas = subpedido_sala.objects.filter(pedido_ptr_id=pedidos.id)
        for sala in salas:
            if sala.acao == 3 and sala.numero_alunos is None:
                writer.writerow(['Descricao', 'inicio', 'fim', 'acao', 'Sala Especifica', 'Numero de alunos' ])
                writer.writerow([sala.editar_descricao, sala.editar_inicio, sala.editar_fim, Acao.objects.get(id=sala.acao).acao, Sala.objects.get(id=sala.editar_id_sala).descricao_sala, "0"])
            elif(sala.acao == 3):
                writer.writerow(['Descricao', 'inicio', 'fim', 'instituicao', 'edificio','numero de alunos', 'acao'])
                writer.writerow([sala.editar_descricao, sala.editar_inicio,sala.editar_fim, Instituicao.objects.get(id = sala.editar_id_instituicao).nome_instituicao, Edificio.objects.get(id=sala.editar_id_edificio).edificio, sala.editar_numero_alunos, Acao.objects.get(id=sala.acao).acao])
            elif(sala.numero_alunos is None):
                writer.writerow(['Descricao', 'inicio', 'fim', 'acao', 'sala especifica', 'Numero de alunos'])
                writer.writerow([sala.descricao, sala.inicio, sala.fim, Acao.objects.get(id=sala.acao).acao, Sala.objects.get(id=sala.id_sala).descricao_sala, "0"])
            else:
                writer.writerow(['Descricao', 'inicio', 'fim', 'instituicao', 'edificio', 'numero de alunos', 'acao'])
                writer.writerow([sala.descricao, sala.inicio, sala.fim, Instituicao.objects.get(id = sala.id_instituicao).nome_instituicao, Edificio.objects.get(id=sala.id_edificio).edificio, sala.numero_alunos, Acao.objects.get(id=sala.acao).acao])
    elif(str(pedidos.tipo) == "TipoDePedido object (4)"):
        writer.writerow([pedidos.assunto, pedidos.data_de_alvo, pedidos.informacoes, 'Unidade Curricular'])
        uc = SubpedidoUc.objects.filter(pedido_ptr_id=pedidos.id)
        writer.writerow(['Acao','Unidade Curricular', 'Turma', 'Descricao'])
        for ucs in uc:
            writer.writerow([ucs.acao, Uc.objects.get(id=ucs.ucid).disciplina, ucs.turma, ucs.descricao])
    writer.writerow([])
    
    return response


def exportar_todos_pedidos_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=pedidos.csv'
    writer = csv.writer(response)
    user = get_user(request)
    if user.groups.filter(name = "Docente").exists():
        docente = Docente.objects.get(pk=request.user.id)
        pedido = Pedido.objects.filter(docenteutilizadorid=docente)
    else:
        pedido = Pedido.objects.all()
    for pedidos in pedido:
        writer.writerow(['Assunto', 'Data Alvo', 'Descricao', 'Tipo de Pedido'])
        if (str(pedidos.tipo) == "TipoDePedido object (1)"):
            writer.writerow([pedidos.assunto, pedidos.data_de_alvo, pedidos.informacoes, 'Horario'])
            horario = Horario.objects.filter(pedido_ptr_id=pedidos.id)
            writer.writerow(['Data Horario', 'Hora inicial', 'Hora final', 'Descricao'])
            for horarios in horario:
                writer.writerow([horarios.data_h, horarios.hora_inicial, horarios.hora_final, horarios.descricao])
        elif(str(pedidos.tipo) == "TipoDePedido object (2)"):
            writer.writerow([pedidos.assunto, pedidos.data_de_alvo, pedidos.informacoes, 'Outros'])
            outros = Outros.objects.filter(pedido_ptr_id=pedidos.id)
            writer.writerow(['Assunto', 'Descrição'])
            for outro in outros:
                writer.writerow([outro.Assunto, outro.Descricao])
        elif(str(pedidos.tipo) == "TipoDePedido object (3)"):
            writer.writerow([pedidos.assunto, pedidos.data_de_alvo, pedidos.informacoes, 'Sala'])
            salas = subpedido_sala.objects.filter(pedido_ptr_id=pedidos.id)
            for sala in salas:
                if sala.acao == 3 and sala.numero_alunos is None:
                    writer.writerow(['Descricao', 'inicio', 'fim', 'acao', 'Sala Especifica', 'Numero de alunos' ])
                    writer.writerow([sala.editar_descricao, sala.editar_inicio, sala.editar_fim, Acao.objects.get(id=sala.acao).acao, Sala.objects.get(id=sala.editar_id_sala).descricao_sala, "0"])
                elif(sala.acao == 3):
                    writer.writerow(['Descricao', 'inicio', 'fim', 'instituicao', 'edificio','numero de alunos', 'acao'])
                    writer.writerow([sala.editar_descricao, sala.editar_inicio,sala.editar_fim, Instituicao.objects.get(id = sala.editar_id_instituicao).nome_instituicao, Edificio.objects.get(id=sala.editar_id_edificio).edificio, sala.editar_numero_alunos, Acao.objects.get(id=sala.acao).acao])
                elif(sala.numero_alunos is None):
                    writer.writerow(['Descricao', 'inicio', 'fim', 'acao', 'sala especifica', 'Numero de alunos'])
                    writer.writerow([sala.descricao, sala.inicio, sala.fim, Acao.objects.get(id=sala.acao).acao, Sala.objects.get(id=sala.id_sala).descricao_sala, "0"])
                else:
                    writer.writerow(['Descricao', 'inicio', 'fim', 'instituicao', 'edificio', 'numero de alunos', 'acao'])
                    writer.writerow([sala.descricao, sala.inicio, sala.fim, Instituicao.objects.get(id = sala.id_instituicao).nome_instituicao, Edificio.objects.get(id=sala.id_edificio).edificio, sala.numero_alunos, Acao.objects.get(id=sala.acao).acao])
        elif(str(pedidos.tipo) == "TipoDePedido object (4)"):
            writer.writerow([pedidos.assunto, pedidos.data_de_alvo, pedidos.informacoes, 'Unidade Curricular'])
            uc = SubpedidoUc.objects.filter(pedido_ptr_id=pedidos.id)
            writer.writerow(['Acao','Unidade Curricular', 'Turma', 'Descricao'])
            for ucs in uc:
                writer.writerow([ucs.acao, Uc.objects.get(id=ucs.ucid).disciplina, ucs.turma, ucs.descricao])
        
        writer.writerow([])


    return response


def exportar_pedidos_pdf(request,id):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica", 14)

    pedidos = Pedido.objects.get(id=id) 
    lines = []
    lines.append("Docente: " + str(pedidos.docenteutilizadorid))
    lines.append("Assunto: " + pedidos.assunto)
    lines.append("Data Alvo: " + pedidos.data_de_alvo.strftime('%d/%m/%Y'))
    lines.append("Descrição: " + pedidos.informacoes)
    if (str(pedidos.tipo) == "TipoDePedido object (1)"):
        horario = Horario.objects.filter(pedido_ptr_id=pedidos.id)
        lines.append("Tipo do pedido: Horário")
        lines.append("")
        lines.append("Subpedidos:")
        for horarios in horario:
            lines.append("")
            lines.append("      Ação: " + horarios.acao)
            if (horarios.acao == "alterar"):
                lines.append("      Data do horário antigo: " + horarios.antigodata_h.strftime('%Y-%m-%d'))
                lines.append("      Hora inicial antiga: " + horarios.antigohora_inicial.strftime('%H:%M'))
                lines.append("      Hora final antiga: " + horarios.antigohora_final.strftime('%H:%M'))
                lines.append("      Descrição do horário antigo: " + horarios.antigodescricao)
                lines.append("      Data do horário: " + horarios.data_h.strftime('%Y-%m-%d'))
                lines.append("      Hora inicial: " + horarios.hora_inicial.strftime('%H:%M'))
                lines.append("      Hora final: " + horarios.hora_final.strftime('%H:%M'))
                lines.append("      Descrição do horário: " + horarios.descricao)
            else:
                lines.append("      Data do horário: " + horarios.data_h.strftime('%Y-%m-%d'))
                lines.append("      Hora inicial: " + horarios.hora_inicial.strftime('%H:%M'))
                lines.append("      Hora final: " + horarios.hora_final.strftime('%H:%M'))
                lines.append("      Descrição do horário: " + horarios.descricao)
    elif(str(pedidos.tipo) == "TipoDePedido object (2)"):
        outros = Outros.objects.filter(pedido_ptr_id=pedidos.id)
        lines.append("Tipo do pedido: Outros")
        lines.append("")
        lines.append("Subpedidos:")
        for outro in outros:
            lines.append("")
            lines.append("      Assunto: " + outro.Assunto)
            lines.append("      Descricao: " + outro.Descricao)
    elif(str(pedidos.tipo) == "TipoDePedido object (3)"):
        salas = subpedido_sala.objects.filter(pedido_ptr_id=pedidos.id)
        lines.append("Tipo do pedido: Sala")
        lines.append("")
        lines.append("Subpedidos:")
        for sala in salas:
            if sala.acao ==3 and sala.numero_alunos is None:
                lines.append("")
                lines.append("      Descrição: " + sala.descricao)
                lines.append("      Descrição nova: " + sala.editar_descricao)
                lines.append("      Inicio: " + sala.inicio.strftime('%Y/%m/%d %H:%M'))
                lines.append("      Inicio novo: " + sala.editar_inicio.strftime('%Y/%m/%d %H:%M'))
                lines.append("      Fim: " + sala.fim.strftime('%Y/%m/%d %H:%M'))
                lines.append("      Fim novo: " + sala.editar_fim.strftime('%Y/%m/%d %H:%M'))
                lines.append("      Ação: " + Acao.objects.get(id=sala.acao).acao )
                lines.append("      Sala Especifica: " + Sala.objects.get(id=sala.id_sala).descricao_sala)
                lines.append("      Sala Especifica nova: " + Sala.objects.get(id=sala.editar_id_sala).descricao_sala)
                lines.append("      Número de alunos: 0" )
            elif(sala.acao == 3):
                lines.append("")
                lines.append("      Descrição: " + sala.descricao)
                lines.append("      Descrição nova: " + sala.editar_descricao)
                lines.append("      Inicio: " + sala.inicio.strftime('%Y/%m/%d %H:%M'))
                lines.append("      Inicio novo: " + sala.editar_inicio.strftime('%Y/%m/%d %H:%M'))
                lines.append("      Fim: " + sala.fim.strftime('%Y/%m/%d %H:%M'))
                lines.append("      Fim novo: " + sala.editar_fim.strftime('%Y/%m/%d %H:%M'))
                lines.append("      Instituição: " + Instituicao.objects.get(id=sala.id_instituicao).nome_instituicao)
                lines.append("      Instituição nova: " + Instituicao.objects.get(id=sala.editar_id_instituicao).nome_instituicao)
                lines.append("      Edificio: " + Edificio.objects.get(id=sala.id_edificio).edificio)
                lines.append("      Edificio novo: " + Edificio.objects.get(id=sala.editar_id_edificio).edificio)
                lines.append("      Tipo de sala: " + Categoria.objects.get(id=sala.categoria).tipo_de_sala)
                lines.append("      Tipo de sala novo: " + Categoria.objects.get(id=sala.editar_categoria).tipo_de_sala)
                lines.append("      Número de alunos: " + str(sala.numero_alunos))
                lines.append("      Número de alunos novo: " + str(sala.editar_numero_alunos))
                lines.append("      Ação: " + Acao.objects.get(id=sala.acao).acao )
            elif(sala.numero_alunos is None):
                lines.append("")
                lines.append("      Descrição: " + sala.descricao)
                lines.append("      Inicio: " + sala.inicio.strftime('%Y/%m/%d %H:%M'))
                lines.append("      Fim: " + sala.fim.strftime('%Y/%m/%d %H:%M'))
                lines.append("      Ação: " + Acao.objects.get(id=sala.acao).acao  )
                lines.append("      Sala Especifica: " + Sala.objects.get(id=sala.id_sala).descricao_sala)
                lines.append("      Número de alunos: 0" )
            else:
                lines.append("")
                lines.append("      Descrição: " + sala.descricao)
                lines.append("      Inicio: " + sala.inicio.strftime('%Y/%m/%d %H:%M'))
                lines.append("      Fim: " + sala.fim.strftime('%Y/%m/%d %H:%M'))
                lines.append("      Instituição: " + Instituicao.objects.get(id=sala.id_instituicao).nome_instituicao)
                lines.append("      Edificio: " + Edificio.objects.get(id=sala.id_edificio).edificio)
                lines.append("      Tipo de sala: " + Categoria.objects.get(id=sala.categoria).tipo_de_sala)
                lines.append("      Número de alunos: " + str(sala.numero_alunos))
                lines.append("      Ação: " + Acao.objects.get(id=sala.acao).acao )     
    elif(str(pedidos.tipo) == "TipoDePedido object (4)"):
        uc = SubpedidoUc.objects.filter(pedido_ptr_id=pedidos.id)
        lines.append("Tipo do pedido: Unidade Curricular")
        lines.append("")
        lines.append("Subpedidos:")
        for ucs in uc:
            lines.append("")
            lines.append("      Ação: " + ucs.acao)
            lines.append("      Unidade Curricular: " + Uc.objects.get(id=ucs.ucid).disciplina)
            lines.append("      Turma: " + ucs.turma)
            lines.append("      Descrição: " + ucs.descricao)
    lines.append("------------------------------------------------------------------------------------------------------")
    lines.append(" ")
    for line in lines:
        textob.textLine(line)
    
    c.drawText(textob)
    c.showPage()  
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename="pedido_"+pedidos.assunto+".pdf")


def exportar_todos_pedidos_pdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica", 14)
    user = get_user(request)
    if user.groups.filter(name = "Docente").exists():
        docente = Docente.objects.get(pk=request.user.id)   
        pedido = Pedido.objects.filter(docenteutilizadorid=docente)
    else:
        pedido = Pedido.objects.all()
    lines = []
    for pedidos in pedido:
        lines.append("Assunto: " + pedidos.assunto)
        lines.append("Data Alvo: " + pedidos.data_de_alvo.strftime('%d/%m/%Y'))
        lines.append("Descrição: " + pedidos.informacoes)

        if (str(pedidos.tipo) == "TipoDePedido object (1)"):
            horario = Horario.objects.filter(pedido_ptr_id=pedidos.id)
            lines.append("Tipo do pedido: Horário")
            lines.append("")
            lines.append("Subpedidos:")
            for horarios in horario:
                lines.append("")
                lines.append("      Data do horário: " + horarios.data_h.strftime('%Y-%m-%d'))
                lines.append("      Hora inicial: " + horarios.hora_inicial.strftime('%H:%M'))
                lines.append("      Hora final: " + horarios.hora_final.strftime('%H:%M'))
                lines.append("      Descrição do horário: " + horarios.descricao)
        elif(str(pedidos.tipo) == "TipoDePedido object (2)"):
            outros = Outros.objects.filter(pedido_ptr_id=pedidos.id)
            lines.append("Tipo do pedido: Outros")
            lines.append("")
            lines.append("Subpedidos:")
            for outro in outros:
                lines.append("")
                lines.append("      Assunto: " + outro.Assunto)
                lines.append("      Descricao: " + outro.Descricao)
        elif(str(pedidos.tipo) == "TipoDePedido object (3)"):
            salas = subpedido_sala.objects.filter(pedido_ptr_id=pedidos.id)
            lines.append("Tipo do pedido: Sala")
            lines.append("")
            lines.append("Subpedidos:")
            for sala in salas:
                if sala.acao ==3 and sala.numero_alunos is None:
                    lines.append("")
                    lines.append("      Descrição: " + sala.descricao)
                    lines.append("      Descrição nova: " + sala.editar_descricao)
                    lines.append("      Inicio: " + sala.inicio.strftime('%Y/%m/%d %H:%M'))
                    lines.append("      Inicio novo: " + sala.editar_inicio.strftime('%Y/%m/%d %H:%M'))
                    lines.append("      Fim: " + sala.fim.strftime('%Y/%m/%d %H:%M'))
                    lines.append("      Fim novo: " + sala.editar_fim.strftime('%Y/%m/%d %H:%M'))
                    lines.append("      Ação: " + Acao.objects.get(id=sala.acao).acao )
                    lines.append("      Sala Especifica: " + Sala.objects.get(id=sala.id_sala).descricao_sala)
                    lines.append("      Sala Especifica nova: " + Sala.objects.get(id=sala.editar_id_sala).descricao_sala)
                    lines.append("      Número de alunos: 0" )
                elif(sala.acao == 3):
                    lines.append("")
                    lines.append("      Descrição: " + sala.descricao)
                    lines.append("      Descrição nova: " + sala.editar_descricao)
                    lines.append("      Inicio: " + sala.inicio.strftime('%Y/%m/%d %H:%M'))
                    lines.append("      Inicio novo: " + sala.editar_inicio.strftime('%Y/%m/%d %H:%M'))
                    lines.append("      Fim: " + sala.fim.strftime('%Y/%m/%d %H:%M'))
                    lines.append("      Fim novo: " + sala.editar_fim.strftime('%Y/%m/%d %H:%M'))
                    lines.append("      Instituição: " + Instituicao.objects.get(id=sala.id_instituicao).nome_instituicao)
                    lines.append("      Instituição nova: " + Instituicao.objects.get(id=sala.editar_id_instituicao).nome_instituicao)
                    lines.append("      Edificio: " + Edificio.objects.get(id=sala.id_edificio).edificio)
                    lines.append("      Edificio novo: " + Edificio.objects.get(id=sala.editar_id_edificio).edificio)
                    lines.append("      Tipo de sala: " + Categoria.objects.get(id=sala.categoria).tipo_de_sala)
                    lines.append("      Tipo de sala novo: " + Categoria.objects.get(id=sala.editar_categoria).tipo_de_sala)
                    lines.append("      Número de alunos: " + str(sala.numero_alunos))
                    lines.append("      Número de alunos novo: " + str(sala.editar_numero_alunos))
                    lines.append("      Ação: " + Acao.objects.get(id=sala.acao).acao )
                elif(sala.numero_alunos is None):
                    lines.append("")
                    lines.append("      Descrição: " + sala.descricao)
                    lines.append("      Inicio: " + sala.inicio.strftime('%Y/%m/%d %H:%M'))
                    lines.append("      Fim: " + sala.fim.strftime('%Y/%m/%d %H:%M'))
                    lines.append("      Ação: " +Acao.objects.get(id=sala.acao).acao )
                    lines.append("      Sala Especifica: " + Sala.objects.get(id=sala.id_sala).descricao_sala)
                    lines.append("      Número de alunos: 0" )
                else:
                    lines.append("")
                    lines.append("      Descrição: " + sala.descricao)
                    lines.append("      Inicio: " + sala.inicio.strftime('%Y/%m/%d %H:%M'))
                    lines.append("      Fim: " + sala.fim.strftime('%Y/%m/%d %H:%M'))
                    lines.append("      Instituição: " + Instituicao.objects.get(id=sala.id_instituicao).nome_instituicao)
                    lines.append("      Edificio: " + Edificio.objects.get(id=sala.id_edificio).edificio)
                    lines.append("      Tipo de sala: " + Categoria.objects.get(id=sala.categoria).tipo_de_sala)
                    lines.append("      Número de alunos: " + str(sala.numero_alunos))
                    lines.append("      Ação: " + Acao.objects.get(id=sala.acao).acao )                           
        elif(str(pedidos.tipo) == "TipoDePedido object (4)"):
            uc = SubpedidoUc.objects.filter(pedido_ptr_id=pedidos.id)
            lines.append("Tipo do pedido: Unidade Curricular")
            lines.append("")
            lines.append("Subpedidos:")
            for ucs in uc:
                lines.append("")
                lines.append("      Ação: " + ucs.acao)
                lines.append("      Unidade Curricular: " + Uc.objects.get(id=ucs.ucid).disciplina)
                lines.append("      Turma: " + ucs.turma)
                lines.append("      Descrição: " + ucs.descricao)
        lines.append(" ")
        lines.append("------------------------------------------------------------------------------------------------------")
        lines.append(" ")
    for line in lines:
        if line == "------------------------------------------------------------------------------------------------------":
            c.drawText(textob)
            c.showPage()
            textob = c.beginText()
            textob.setTextOrigin(inch,inch)
            textob.setFont("Helvetica", 14)
        else:
            textob.textLine(line)
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename="pedidos.pdf")



def associar_pedido_funcionario(request,id):
    pedido = Pedido.objects.get(id=id)
    user = get_user(request)
    if user.groups.filter(name = "Funcionario").exists():
        if request.method == 'POST':
                if 'confirmar' in request.POST:
                    pedido.funcionarioutilizadorid = Funcionario.objects.get(utilizador_ptr_id=user.id)
                    pedido.estado_0 = EstadoPedido.objects.get(id=2)
                    pedido.data_de_associacao = datetime.datetime.today()
                    pedido.save()
                    return redirect('main:mensagem',12)
                else:
                    return redirect('pedidos:listagem-pedidos')
        else:
            return render(request, 'pedido/associar_pedido_funcionario.html', {'pedido_id': id})

    return render(request, 'pedido/associar_pedido_funcionario.html', {'pedido_id': id})



def desassociar_pedido_funcionario(request,id):
    pedido = Pedido.objects.get(id=id)
    user = get_user(request)
    if user.groups.filter(name="Funcionario").exists():
        if request.method == 'POST':
                if 'confirmar' in request.POST:
                    pedido.funcionarioutilizadorid = None
                    pedido.estado_0 = EstadoPedido.objects.get(id=1)
                    pedido.data_de_associacao = None
                    pedido.save()
                    return redirect('main:mensagem',22)
                else:
                    return redirect('pedidos:listagem-pedidos')
        else:
            return render(request, 'pedido/desassociar_pedido_funcionario.html', {'pedido_id': id})

    return render(request, 'pedido/desassociar_pedido_funcionario.html', {'pedido_id': id})


####################################################################################################################
################### Inicio           de criar Pedido Outros                 ########################################
####################################################################################################################
def criar_pedidos_outros(request):
    erros = ""
    msg = ""
    user = get_user(request)
    if user.groups.filter(name = "Docente").exists():
        if request.method == 'POST':
            subpedidos = json.loads(request.POST['subpedidos'])
            form = PedidoOutrosForm(request.POST)
            descricao = request.POST.get('informacoes', '')
            assunto = request.POST.get('assunto', '')
            data = request.POST.get('data', '') 
            opcao = request.POST.get('selected_option')
            print(opcao)
            #Verificação da data
            try:
                data = datetime.datetime.strptime(data, '%Y-%m-%d').date()
                hoje = datetime.date.today()
                data_destino =  ano_letivo.objects.get(ativo="S").dia_fim
                if data < hoje or data > data_destino:
                    erros = "A data deve estar entre hoje e fim do ano letivo( "+ str(data_destino) + ")";
                    msg = True
                    return render(request, 
                        template_name="pedido/criar_pedido_outros.html",
                        context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos})
            except ValueError:
                erros = "Data inválida."
                msg = True
                return render(request, 
                    template_name="pedido/criar_pedido_outros.html",
                    context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos})
            
            
            if opcao == "1":
                if(subpedidos == []):
                    erros = "Têm que haver pelo menos um subpedido"
                    msg = True
                    return render(request, 
                        template_name="pedido/criar_pedido_outros.html",
                        context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos})
            elif opcao == "2":
                arquivo = request.FILES['arquivo']
                if str(arquivo).endswith(".xls") :
                    print("Ficheiro correto")
                else:
                    erros = "Ficheiro têm de ser do tipo .xls"
                    msg = True
                    return render(request, 
                        template_name="pedido/criar_pedido_outros.html",
                        context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos})
                
            #Verificação do assunto
            if len(assunto) < 5:
                erros = "Assunto têm de ter mais que 5 caracteres."
                msg = True
                return render(request, 
                    template_name="pedido/criar_pedido_outros.html",
                    context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos})
            
            #Verificação da descricao geral
            elif len(descricao) < 5:
                erros = "Informações têm de ter mais que 5 caracteres."
                msg = True
                return render(request, 
                    template_name="pedido/criar_pedido_outros.html",
                    context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos})
        

            
            if form.is_valid():
                #Verificacao se existe duplicação de Pedidos na BD
                try:
                    PedidoOutros.objects.get(docenteutilizadorid=request.user.id, data_de_alvo=data, assunto=assunto)
                    erros = "Já existe um pedido com esta data e assunto."
                    msg = True
                    return render(request, template_name="pedido/criar_pedido_outros.html",
                        context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos})
                
                except ObjectDoesNotExist:
                    pedido = form.save(commit=False)
                    pedido.estado_0 = EstadoPedido.objects.get(id=1)
                    pedido.docenteutilizadorid = Docente.objects.get(utilizador_ptr_id=request.user.id)
                    pedido.data_de_submissao = datetime.date.today()
                    pedido.data_de_alvo = data
                    pedido.identificador_id = IdentificadorPedido.objects.get(id=opcao)
                    pedido.tipo = TipoDePedido.objects.get(id=2)
                    pedido.assunto = assunto
                    pedido.anoletivoid = ano_letivo.objects.get(ativo="S")
                    pedido.informacoes = descricao 
                    pedido.save()   
                    if opcao == "2":
                        ficheiros_dir = os.path.join(settings.BASE_DIR, 'ficheiros')
                        ficheiro_nome = f'pedido_{pedido.id}.{arquivo.name.split(".")[-1]}'
                        with open(os.path.join(ficheiros_dir, ficheiro_nome), 'wb') as f:
                            for chunk in arquivo.chunks():
                                f.write(chunk)
                    elif opcao == "1":
                        for subpedido in subpedidos:
                            outros = Outros(Assunto=subpedido['assunto'],
                                            Descricao=subpedido['descricao'],
                                            pedido_ptr_id=pedido.id)
                            outros.save()
                    
                    funcionarios = Funcionario.objects.all()
                    mensagem_para_email = "O docente " + str(user) + " registou um novo Pedido Outros."
                    for x in funcionarios:
                        user_recipient = x
                        info = InformacaoMensagem(data=timezone.now(), pendente=True, titulo = "Registo de novo pedido Outros",
                                        descricao =mensagem_para_email, emissor = user , recetor = user_recipient, tipo = "Grupo" , lido = False)
                        info.save()
                        if user_recipient.id != user.id:
                            tmp = MensagemRecebida(mensagem=info)
                            tmp.save() 

                    mensagem1 = MensagemEnviada(mensagem=info)
                    mensagem1.mensagem.lido = False
                    mensagem1.save() 
                    pedidos = Pedido.objects.all().order_by('-id')
                    num_pedidos = 0
                    for pedido in pedidos:
                        if pedido.estado_0.id == 1:
                            num_pedidos+=1;
                    msg_automatica = "Ainda têm " + str(num_pedidos-1) + " pedidos pela frente."
                    info = InformacaoMensagem(data=timezone.now(), pendente=False, titulo = "Pedido Criado com sucesso",
                                descricao = msg_automatica,  recetor = user, tipo = "Individual" , lido = False) 
                    info.save()
                    tmp = MensagemRecebida(mensagem=info)
                    tmp.save() 

                    return redirect('main:mensagem',4)
        else:
            form = PedidoOutrosForm()
            msg = False
        
        return render(request, 
                    template_name="pedido/criar_pedido_outros.html",
                    context={'erros': erros,'msg':msg,'form':form})
    else:
        return redirect('main:mensagem',222)


####################################################################################################################
################### Fim de criar Pedido Outros                 ####################################3333
####################################################################################################################

####################################################################################################################
################### Inicio de Editar Pedido Outros                 ####################################3333
####################################################################################################################
def editar_pedidos_outros(request,id):
    erros = ""
    if request.method == 'POST':
        subpedidos = json.loads(request.POST['subpedidos'])
        form = PedidoOutrosForm(request.POST)
        descricao = request.POST.get('informacoes', '')
        assunto = request.POST.get('assunto', '')
        data = request.POST.get('data', '') 
        opcao = request.POST.get('selected_option')
        print(opcao)
        try:
            data = datetime.datetime.strptime(data, '%Y-%m-%d').date()
            hoje = datetime.date.today()
            data_destino =  ano_letivo.objects.get(ativo="S").dia_fim
            if data < hoje or data > data_destino:
                erros = "A data deve estar entre hoje e fim do ano letivo( "+ str(data_destino) + ")";
                msg = True
                return render(request, 
                    template_name="pedido/criar_pedido_outros.html",
                    context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos})
        except ValueError:
            erros = "Data inválida."
            msg = True
            return render(request, 
                template_name="pedido/criar_pedido_outros.html",
                context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos})
            
        arquivo= "2"

        if opcao == "1":
            if(subpedidos == []):
                erros = "Têm que haver pelo menos um subpedido"
                msg = True
                return render(request, 
                    template_name="pedido/criar_pedido_outros.html",
                    context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos})
        elif opcao == "2":
            if 'arquivo' in request.FILES:
                arquivo = request.FILES['arquivo']
                if str(arquivo).endswith(".xls"):
                    print("Ficheiro correto")
                else:
                    erros = "Ficheiro têm de ser do tipo .xls"
                    msg = True
                    return render(request, 
                        template_name="pedido/criar_pedido_outros.html",
                        context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos})
            else:
                arquivo = ""

        if len(assunto) < 5:
            erros = "Assunto têm de ter mais que 5 caracteres."
            msg = True
            return render(request, 
                  template_name="pedido/editar_pedido_outros.html",
                  context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos})
        elif len(descricao) < 5:
            erros = "Descrição têm de ter mais que 5 caracteres."
            msg = True
            return render(request, 
                  template_name="pedido/editar_pedido_outros.html",
                  context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos})
        if form.is_valid():
            pedido = PedidoOutros.objects.get(id=id) 
            pedido.data_de_submissao = datetime.date.today()
            pedido.data_de_alvo = data
            pedido.tipo = TipoDePedido.objects.get(id=2)
            pedido.assunto = assunto
            pedido.anoletivoid = ano_letivo.objects.get(ativo="S")
            pedido.informacoes = descricao 
            
            if pedido.identificador_id.id == 2 and arquivo != "":
                ficheiros_dir = os.path.join(settings.BASE_DIR, 'ficheiros\pedido_') 
                ficheiros_dir = str(ficheiros_dir)+ str(id) + ".xls"
                os.remove(ficheiros_dir)
            elif pedido.identificador_id.id == 1:
                Outros.objects.filter(pedido_ptr_id=id).delete()

            pedido.identificador_id = IdentificadorPedido.objects.get(id=opcao)
            pedido.save()   
            if opcao == "2" and arquivo != "":
                ficheiros_dir = os.path.join(settings.BASE_DIR, 'ficheiros')
                ficheiro_nome = f'pedido_{pedido.id}.{arquivo.name.split(".")[-1]}'
                with open(os.path.join(ficheiros_dir, ficheiro_nome), 'wb') as f:
                    for chunk in arquivo.chunks():
                        f.write(chunk)
            elif opcao == "1":
                Outros.objects.filter(pedido_ptr_id=id).delete()
                for subpedido in subpedidos:
                    outros = Outros(Assunto=subpedido['assunto'],
                                    Descricao=subpedido['descricao'],
                                    pedido_ptr_id=pedido.id)
                    outros.save()
            return redirect('main:mensagem',5)
    else:
        pedidoid = id
        pedido = Pedido.objects.get(id=pedidoid)
        data_alvo = str(pedido.data_de_alvo)
        data_objeto = parser.parse(data_alvo)
        data_formatada = data_objeto.strftime('%Y-%m-%d')
        pedido = Pedido.objects.get(id=id)
        identificador = pedido.identificador_id.id
        subpedidos =[]
        file_url = ""
        if identificador == 1:
            outros = Outros.objects.filter(pedido_ptr_id=id)
            for outro in outros:
                subpedido = {}
                subpedido['assunto'] = outro.Assunto
                subpedido['descricao'] = outro.Descricao
                subpedidos.append(subpedido)
        elif identificador == 2:
            pedido_ficheiro_nome = "pedido_" + str(pedido.id) + ".xls"
            file_url = os.path.join(settings.BASE_DIR, 'ficheiros', pedido_ficheiro_nome)        
        form = PedidoOutrosForm(initial={'informacoes': pedido.informacoes,'data':data_formatada, 'assunto': pedido.assunto})
    msg = ""
    return render(request, 
                  template_name="pedido/editar_pedido_outros.html",
                  context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos,'tipo': identificador,'file_url':file_url})

####################################################################################################################
################### Fim de Editar Pedido Outros                 ####################################3333
####################################################################################################################


####################################################################################################################
################### Incio de Consultar Pedido Outros                 ####################################3333
####################################################################################################################

def consultar_pedido_outros(request,id):
    pedido = Pedido.objects.get(id=id);
    pedido.estado = pedido.estado_0.estado
    pedido.data_de_alvo = pedido.data_de_alvo.strftime('%d/%m/%Y');
    file_url = ""
    if pedido.identificador_id.id == 1:
        outros = Outros.objects.filter(pedido_ptr_id=pedido.id)
        subpedidos = []
        for outro in outros:
            subpedido = {}
            subpedido['assunto'] = outro.Assunto
            subpedido['descricao'] = outro.Descricao
            subpedidos.append(subpedido)
        pedido.subpedidos = subpedidos
    else:
        pedido_ficheiro_nome = "pedido_" + str(pedido.id) + ".xls"
        file_url = os.path.join(settings.BASE_DIR, 'ficheiros', pedido_ficheiro_nome)     
        pedido.fire_url = file_url
    return render(request, 
                        'pedido/consultar_pedido_outros.html',
                        context={'pedido_outros': pedido, 'file_url': file_url })

####################################################################################################################
################### Fim de Consultar Pedido Outros                              ####################################
#####################################################################################################################


####################################################################################################################
################### Fim de Eliminar Pedido Outros                 ####################################3333
####################################################################################################################


def eliminar_pedido_outros(request, id):
    pedido = Pedido.objects.get(id=id)
    user = get_user(request)
    if user.groups.filter(name = "Docente").exists():
        if pedido.estado_0.estado == 'Pendente':
            if request.method == 'POST':
                if 'confirmar' in request.POST:
                    if pedido.identificador_id.id == 1:
                        Outros.objects.filter(pedido_ptr_id=id).delete()
                    else:
                        ficheiros_dir = os.path.join(settings.BASE_DIR, 'ficheiros\pedido_') 
                        ficheiros_dir = str(ficheiros_dir)+ str(id) + ".xls"
                        os.remove(ficheiros_dir)
                    pedido.delete()
                    return redirect('main:mensagem',6)
                else:
                    return redirect('pedidos:listagem-pedidos')
            else:
                return render(request, 'pedido/eliminar_pedido_outros.html', {'pedido_id': id})
        else:
            return redirect('main:mensagem',7)
    elif user.groups.filter(name = "Funcionario").exists():
        return redirect('main:mensagem',8)
    

####################################################################################################################
################### Fim de Eliminar Pedido Outros                              ####################################
#####################################################################################################################






def criar_pedidos_uc(request):
    erros = ""
    msg = ""
    user = get_user(request)
    disciplina = Uc.objects.all()
    disciplinas = []
    nomes_disciplinas = []  
    for d in disciplina:
       if d.disciplina not in nomes_disciplinas:  
        di = {}
        di['id'] = d.id
        di['nome'] = d.disciplina
        disciplinas.append(di)
        nomes_disciplinas.append(d.disciplina)

    if user.groups.filter(name = "Docente").exists():
        if request.method == 'POST':
            subpedidos = json.loads(request.POST['subpedidos'])
            form = PedidoUcForm(request.POST)
            descricao = request.POST.get('descricao', '')
            assunto = request.POST.get('assunto', '')
            data = request.POST.get('data', '') 
            opcao = request.POST.get('selected_option')
            #Verificação da data
            try:
                data = datetime.datetime.strptime(data, '%Y-%m-%d').date()
                hoje = datetime.date.today()
                data_destino =  ano_letivo.objects.get(ativo="S").dia_fim
                if data < hoje or data > data_destino:
                    erros = "A data deve estar entre hoje e fim do ano letivo( "+ str(data_destino) + ")"
                    msg = True
                    return render(request, 
                        template_name="pedido/criar_pedido_uc.html",
                        context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos,'ucs':disciplinas})
            except ValueError:
                erros = "Data inválida."
                msg = True
                return render(request, 
                    template_name="pedido/criar_pedido_uc.html",
                    context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos,'ucs':disciplinas})
            
            if opcao == "1":
                if(subpedidos == []):
                    erros = "Têm que haver pelo menos um subpedido"
                    msg = True
                    return render(request, 
                        template_name="pedido/criar_pedido_uc.html",
                        context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos})
            elif opcao == "2":
                arquivo = request.FILES['arquivo']
                if str(arquivo).endswith(".xls") :
                    print("Ficheiro correto")
                else:
                    erros = "Ficheiro têm de ser do tipo .xls"
                    msg = True
                    return render(request, 
                        template_name="pedido/criar_pedido_uc.html",
                        context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos})


            #Verificação do assunto
            if len(assunto) < 5:
                erros = "Assunto têm de ter mais que 5 caracteres."
                msg = True
                return render(request, 
                    template_name="pedido/criar_pedido_uc.html",
                    context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos,'ucs':disciplinas})
            
            #Verificação da descricao geral
            elif len(descricao) < 5:
                erros = "Informações têm de ter mais que 5 caracteres."
                msg = True
                return render(request, 
                    template_name="pedido/criar_pedido_uc.html",
                    context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos,'ucs':disciplinas})
            
            if form.is_valid():
                #Verificacao se existe duplicação de Pedidos na BD
                try:
                    PedidoUc.objects.get(docenteutilizadorid=request.user.id, data_de_alvo=data, assunto=assunto)
                    erros = "Já existe um pedido com esta data e assunto."
                    msg = True
                    return render(request, template_name="pedido/criar_pedido_uc.html",
                        context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos,'ucs':disciplinas})
                
                except ObjectDoesNotExist:
                    pedido = form.save(commit=False)
                    pedido.estado_0 = EstadoPedido.objects.get(id=1)
                    pedido.docenteutilizadorid = Docente.objects.get(utilizador_ptr_id=request.user.id)
                    pedido.data_de_submissao = datetime.date.today()
                    pedido.data_de_alvo = data
                    pedido.tipo = TipoDePedido.objects.get(id=4)
                    pedido.assunto = assunto
                    pedido.anoletivoid = ano_letivo.objects.get(ativo="S")
                    pedido.informacoes = descricao
                    pedido.identificador_id = IdentificadorPedido.objects.get(id=opcao) 
                    pedido.save()

                    if opcao == "2":
                        ficheiros_dir = os.path.join(settings.BASE_DIR, 'ficheiros')
                        ficheiro_nome = f'pedido_{pedido.id}.{arquivo.name.split(".")[-1]}'
                        with open(os.path.join(ficheiros_dir, ficheiro_nome), 'wb') as f:
                            for chunk in arquivo.chunks():
                                f.write(chunk)
                    elif opcao == "1":
                        for subpedido in subpedidos:
                            uc = SubpedidoUc( ucid=subpedido['uc'].split('_')[0],
                                           acao=subpedido['acao'],
                                          turma=subpedido['turma'],
                                          descricao=subpedido['descricao'],
                                          pedido_ptr_id=pedido.id)
                            uc.save()
                    return redirect('main:mensagem',4)
        else:
            form = PedidoUcForm()
            msg = False

        return render(request, 
                    template_name="pedido/criar_pedido_uc.html",
                    context={'erros': erros,'msg':msg,'form':form,'ucs':disciplinas})
    else:
        return redirect('main:mensagem',222)

def editar_pedidos_uc(request,id):
    erros = ""
    disciplina = Uc.objects.all()
    disciplinas = []
    nomes_disciplinas = []  
    for d in disciplina:
       if d.disciplina not in nomes_disciplinas:  
        di = {}
        di['id'] = d.id
        di['nome'] = d.disciplina
        disciplinas.append(di)
        nomes_disciplinas.append(d.disciplina)
    if request.method == 'POST':
        subpedidos = json.loads(request.POST['subpedidos'])
        form = PedidoUcForm(request.POST)
        descricao = request.POST.get('descricao', '')
        assunto = request.POST.get('assunto', '')
        data = request.POST.get('data', '') 
        opcao = request.POST.get('selected_option')
        try:
            data = datetime.datetime.strptime(data, '%Y-%m-%d').date()
            hoje = datetime.date.today()
            data_destino =  ano_letivo.objects.get(ativo="S").dia_fim
            if data < hoje or data > data_destino:
                erros = "A data deve estar entre hoje e fim do ano letivo( "+ str(data_destino) + ")"
                msg = True
                return render(request, 
                    template_name="pedido/editar_pedido_uc.html",
                    context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos,'ucs':disciplinas})
        except ValueError:
            erros = "Data inválida."
            msg = True
            return render(request, 
                template_name="pedido/editar_pedido_uc.html",
                context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos,'ucs':disciplinas})
        arquivo = "2"
        if opcao == "1":
            if(subpedidos == []):
                erros = "Têm que haver pelo menos um subpedido"
                msg = True
                return render(request, 
                    template_name="pedido/editar_pedido_uc.html",
                    context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos,'ucs':disciplinas})
        elif opcao == "2":
            if 'arquivo' in request.FILES:
                arquivo = request.FILES['arquivo']
                if str(arquivo).endswith(".xls"):
                    print("Ficheiro correto")
                else:
                    erros = "Ficheiro têm de ser do tipo .xls"
                    msg = True
                    return render(request, 
                        template_name="pedido/editar_pedido_uc.html",
                        context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos, 'ucs':disciplinas})
            else:
                arquivo = ""

        if len(assunto) < 5:
            erros = "Assunto têm de ter mais que 5 caracteres."
            msg = True
            return render(request, 
                  template_name="pedido/editar_pedido_uc.html",
                  context={'erros': erros,'msg':msg,'form':form})
        elif len(descricao) < 5:
            erros = "Descrição têm de ter mais que 5 caracteres."
            msg = True
            return render(request, 
                  template_name="pedido/editar_pedido_uc.html",
                  context={'erros': erros,'msg':msg,'form':form, 'pedidos':subpedidos, 'ucs':disciplinas})
        if form.is_valid():
            pedido = PedidoUc.objects.get(id=id)
            pedido.estado_0 = EstadoPedido.objects.get(id=1)
            pedido.docenteutilizadorid = Docente.objects.get(utilizador_ptr_id=request.user.id)
            pedido.data_de_submissao = datetime.date.today()
            pedido.data_de_alvo = data
            pedido.tipo = TipoDePedido.objects.get(id=4)
            pedido.assunto = assunto
            pedido.anoletivoid = ano_letivo.objects.get(ativo="S")
            pedido.informacoes = descricao 
            SubpedidoUc.objects.filter(pedido_ptr_id=id).delete()
            if pedido.identificador_id.id == 2 and arquivo != "":
                ficheiros_dir = os.path.join(settings.BASE_DIR, 'ficheiros\pedido_') 
                ficheiros_dir = str(ficheiros_dir)+ str(id) + ".xls"
                os.remove(ficheiros_dir)
            elif pedido.identificador_id.id == 1:
                SubpedidoUc.objects.filter(pedido_ptr_id=id).delete()

            pedido.identificador_id = IdentificadorPedido.objects.get(id=opcao)
            pedido.save()
            if opcao == "2" and arquivo != "":
                ficheiros_dir = os.path.join(settings.BASE_DIR, 'ficheiros')
                ficheiro_nome = f'pedido_{pedido.id}.{arquivo.name.split(".")[-1]}'
                with open(os.path.join(ficheiros_dir, ficheiro_nome), 'wb') as f:
                    for chunk in arquivo.chunks():
                        f.write(chunk)
            elif opcao == "1":
                SubpedidoUc.objects.filter(pedido_ptr_id=id).delete()
                for subpedido in subpedidos:
                    uc = SubpedidoUc(ucid=subpedido['uc'].split('_')[0],
                                           acao=subpedido['acao'],
                                          turma=subpedido['turma'],
                                          descricao=subpedido['descricao'],
                                          pedido_ptr_id=pedido.id)
                    uc.save()
            return redirect('main:mensagem',5)
    else:
        pedidoid = id
        pedido = Pedido.objects.get(id=pedidoid)
        data_alvo = str(pedido.data_de_alvo)
        data_objeto = parser.parse(data_alvo)
        data_formatada = data_objeto.strftime('%Y-%m-%d')
        pedido = Pedido.objects.get(id=id)
        identificador = pedido.identificador_id.id
        file_url = ""
        subpedidos = []
        if identificador == 1:
            uc = SubpedidoUc.objects.filter(pedido_ptr_id=id)
            for ucs in uc:
                subpedido = {}
                subpedido['acao'] = ucs.acao
                subpedido['uc'] = Uc.objects.get(id=ucs.ucid).id
                subpedido['uc_name'] = Uc.objects.get(id=ucs.ucid).disciplina
                subpedido['turma'] = ucs.turma
                subpedido['descricao'] = ucs.descricao
                subpedidos.append(subpedido)
            pedido.subpedidos = subpedidos
        elif identificador == 2:
            pedido_ficheiro_nome = "pedido_" + str(pedido.id) + ".xls"
            file_url = os.path.join(settings.BASE_DIR, 'ficheiros', pedido_ficheiro_nome)        
        form = PedidoUcForm(initial={'descricao': pedido.informacoes,'data':data_formatada, 'assunto': pedido.assunto})
        msg = ""
        return render(request, 
                  template_name="pedido/editar_pedido_uc.html",
                  context={'erros': erros,'msg':msg,'form':form, 'pedidos':subpedidos, 'tipo': identificador, 'file_url': file_url,'ucs':disciplinas})



def consultar_pedidos_uc(request, id):
    pedido = Pedido.objects.get(id=id)
    pedido.data_de_alvo = pedido.data_de_alvo.strftime('%d/%m/%Y')
    file_url = ''
    
    if pedido.identificador_id.id == 1:
        uc = SubpedidoUc.objects.filter(pedido_ptr_id=pedido.id)
        subpedidos = []
        for ucs in uc:
            subpedido = {}
            subpedido['acao'] = ucs.acao
            subpedido['uc'] = Uc.objects.get(id=ucs.ucid).disciplina
            subpedido['turma'] = ucs.turma
            subpedido['descricao'] = ucs.descricao
            subpedidos.append(subpedido)
        pedido.subpedidos = subpedidos

    else:
        pedido_ficheiro_nome = "pedido_" + str(pedido.id) + ".xls"
        file_url = os.path.join(settings.BASE_DIR, 'ficheiros', pedido_ficheiro_nome)     
        pedido.fire_url = file_url
    return render(request, 
                        'pedido/consultar_pedidos_uc.html',
                        context={'pedido_uc': pedido, 'file_url': file_url })
    

def eliminar_pedido_uc(request, id):
    pedido = Pedido.objects.get(id=id)
    user = get_user(request)
    if user.groups.filter(name = "Docente").exists():
        if pedido.estado_0.estado == 'Pendente':
            if request.method == 'POST':
                if 'confirmar' in request.POST:
                    if pedido.identificador_id.id == 1:
                        SubpedidoUc.objects.filter(pedido_ptr_id=id).delete()
                    else:
                        ficheiros_dir = os.path.join(settings.BASE_DIR, 'ficheiros\pedido_') 
                        ficheiros_dir = str(ficheiros_dir)+ str(id) + ".xls"
                        os.remove(ficheiros_dir)
                    pedido.delete()
                    return redirect('main:mensagem',6)
                else:
                    return redirect('pedidos:listagem-pedidos')
            else:
                return render(request, 'pedido/eliminar_pedido_uc.html', {'pedido_id': id})
        else:
            return redirect('main:mensagem',7)
    elif user.groups.filter(name = "Funcionario").exists():
        return redirect('main:mensagem',8)





####################################################################################################################
################### Inicio           de criar Pedido Horarios                ########################################
####################################################################################################################
def criar_pedidos_horario(request):
    erros = ""
    msg = ""
    user = get_user(request)
    if user.groups.filter(name = "Docente").exists():
        if request.method == 'POST':
            subpedidos = json.loads(request.POST['subpedidos'])
            form = PedidoHorarioForm(request.POST)
            descricao = request.POST.get('descricao', '')
            assunto = request.POST.get('assunto', '')
            data = request.POST.get('data', '') 
            opcao = request.POST.get('selected_option')
            print(opcao)
            #Verificação da data
            try:
                data = datetime.datetime.strptime(data, '%Y-%m-%d').date()
                hoje = datetime.date.today()
                data_destino =  ano_letivo.objects.get(ativo="S").dia_fim
                if data < hoje or data > data_destino:
                    erros = "A data deve estar entre hoje e fim do ano letivo( "+ str(data_destino) + ")"
                    msg = True
                    return render(request, 
                        template_name="pedido/criar_pedido_horario.html",
                        context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos})
            except ValueError:
                erros = "Data inválida."
                msg = True
                return render(request, 
                    template_name="pedido/criar_pedido_horario.html",
                    context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos})
            
            if opcao == "1":
                if(subpedidos == []):
                    erros = "Têm que haver pelo menos um subpedido"
                    msg = True
                    return render(request, 
                        template_name="pedido/criar_pedido_horario.html",
                        context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos})
            elif opcao == "2":
                arquivo = request.FILES['arquivo']
                if str(arquivo).endswith(".xls") :
                    print("Ficheiro correto")
                else:
                    erros = "Ficheiro têm de ser do tipo .xls"
                    msg = True
                    return render(request, 
                        template_name="pedido/criar_pedido_horario.html",
                        context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos})

            #Verificação do assunto
            if len(assunto) < 5:
                erros = "Assunto têm de ter mais que 5 caracteres."
                msg = True
                return render(request, 
                    template_name="pedido/criar_pedido_horario.html",
                    context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos})
            
            #Verificação da descricao geral
            elif len(descricao) < 5:
                erros = "Informações têm de ter mais que 5 caracteres."
                msg = True
                return render(request, 
                    template_name="pedido/criar_pedido_horario.html",
                    context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos})
            
            if form.is_valid():
                #Verificacao se existe duplicação de Pedidos na BD
                try:
                    PedidoDeHorario.objects.get(docenteutilizadorid=request.user.id, data_de_alvo=data, assunto=assunto)
                    erros = "Já existe um pedido com esta data e assunto."
                    msg = True
                    return render(request, template_name="pedido/criar_pedido_horario.html",
                        context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos})
                
                except ObjectDoesNotExist:
                    pedido = form.save(commit=False)
                    pedido.estado_0 = EstadoPedido.objects.get(id=1)
                    pedido.docenteutilizadorid = Docente.objects.get(utilizador_ptr_id=request.user.id)
                    pedido.data_de_submissao = datetime.date.today()
                    pedido.data_de_alvo = data
                    pedido.tipo = TipoDePedido.objects.get(id=1)
                    pedido.identificador_id = IdentificadorPedido.objects.get(id=opcao)
                    pedido.assunto = assunto
                    pedido.anoletivoid = ano_letivo.objects.get(ativo="S")
                    pedido.informacoes = descricao 
                    pedido.save()   
                    if opcao == "2":
                        ficheiros_dir = os.path.join(settings.BASE_DIR, 'ficheiros')
                        ficheiro_nome = f'pedido_{pedido.id}.{arquivo.name.split(".")[-1]}'
                        with open(os.path.join(ficheiros_dir, ficheiro_nome), 'wb') as f:
                            for chunk in arquivo.chunks():
                                f.write(chunk)
                    elif opcao == "1":
                        for subpedido in subpedidos:
                            if (subpedido['acoes'] == "alterar"):
                                horario = Horario(acao = subpedido['acoes'],
                                              data_h=subpedido['date_h'],
                                              hora_inicial=subpedido['timeinicial'],
                                              hora_final=subpedido['timefinal'],
                                              descricao=subpedido['descricao'],
                                              antigodata_h=subpedido['antigodate_h'],
                                              antigohora_inicial=subpedido['antigotimeinicial'],
                                              antigohora_final=subpedido['antigotimefinal'],
                                              antigodescricao=subpedido['antigodescricao'],
                                              pedido_ptr_id=pedido.id)
                            else:
                                horario = Horario(acao = subpedido['acoes'],
                                              data_h=subpedido['date_h'],
                                              hora_inicial=subpedido['timeinicial'],
                                              hora_final=subpedido['timefinal'],
                                              descricao=subpedido['descricao'],
                                              pedido_ptr_id=pedido.id)
                            horario.save()
                    funcionarios = Funcionario.objects.all()
                    mensagem_para_email = "O docente " + str(user) + " registou um novo Pedido de Horário."
                    for x in funcionarios:
                        user_recipient = x
                        info = InformacaoMensagem(data=timezone.now(), pendente=True, titulo = "Registo de novo pedido de Horário",
                                        descricao =mensagem_para_email, emissor = user , recetor = user_recipient, tipo = "Grupo" , lido = False)
                        info.save()
                        if user_recipient.id != user.id:
                            tmp = MensagemRecebida(mensagem=info)
                            tmp.save() 

                    mensagem1 = MensagemEnviada(mensagem=info)
                    mensagem1.mensagem.lido = False
                    mensagem1.save() 
                    num_pedidos = 2 #Falta calcular o tempo medio e o numerp de pedidos
                    msg_automatica = "Ainda têm " + str(num_pedidos) + " pedidos pela frente."
                    info = InformacaoMensagem(data=timezone.now(), pendente=False, titulo = "Pedido Criado com sucesso",
                                descricao = msg_automatica,  recetor = user, tipo = "Individual" , lido = False) 
                    info.save()
                    tmp = MensagemRecebida(mensagem=info)
                    tmp.save() 

                    return redirect('main:mensagem',4)
        else:
            form = PedidoHorarioForm()
            msg = False

        return render(request, 
                    template_name="pedido/criar_pedido_horario.html",
                    context={'erros': erros,'msg':msg,'form':form})
    else:
        return redirect('main:mensagem',222)


####################################################################################################################
################### Fim de criar Pedido Horario                 ####################################3333
####################################################################################################################


def editar_pedidos_horario(request,id):
    erros = ""
    if request.method == 'POST':
        subpedidos = json.loads(request.POST['subpedidos'])
        form = PedidoHorarioForm(request.POST)
        descricao = request.POST.get('descricao', '')
        assunto = request.POST.get('assunto', '')
        data = request.POST.get('data', '') 
        opcao = request.POST.get('selected_option')
        print(opcao)
        try:
            data = datetime.datetime.strptime(data, '%Y-%m-%d').date()
            hoje = datetime.date.today()
            data_destino =  ano_letivo.objects.get(ativo="S").dia_fim
            if data < hoje or data > data_destino:
                erros = "A data deve estar entre hoje e fim do ano letivo( "+ str(data_destino) + ")"
                msg = True
                return render(request, 
                    template_name="pedido/criar_pedido_horario.html",
                    context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos})
        except ValueError:
            erros = "Data inválida."
            msg = True
            return render(request, 
                template_name="pedido/criar_pedido_horario.html",
                context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos})
        arquivo = "2"

        if opcao == "1":
            if(subpedidos == []):
                erros = "Têm que haver pelo menos um subpedido"
                msg = True
                return render(request, 
                    template_name="pedido/criar_pedido_outros.html",
                    context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos})
        elif opcao == "2":
            if 'arquivo' in request.FILES:
                arquivo = request.FILES['arquivo']
                if str(arquivo).endswith(".xls"):
                    print("Ficheiro correto")
                else:
                    erros = "Ficheiro têm de ser do tipo .xls"
                    msg = True
                    return render(request, 
                        template_name="pedido/criar_pedido_outros.html",
                        context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos})
            else:
                arquivo = ""

        if len(assunto) < 5:
            erros = "Assunto têm de ter mais que 5 caracteres."
            msg = True
            return render(request, 
                  template_name="pedido/editar_pedido_horario.html",
                  context={'erros': erros,'msg':msg,'form':form})
        elif len(descricao) < 5:
            erros = "Descrição têm de ter mais que 5 caracteres."
            msg = True
            return render(request, 
                  template_name="pedido/editar_pedido_horario.html",
                  context={'erros': erros,'msg':msg,'form':form, 'pedidos':subpedidos})
        if form.is_valid():
            pedido = PedidoDeHorario.objects.get(id=id)
            pedido.estado_0 = EstadoPedido.objects.get(id=1)
            pedido.docenteutilizadorid = Docente.objects.get(utilizador_ptr_id=request.user.id)
            pedido.data_de_submissao = datetime.date.today()
            pedido.data_de_alvo = data
            pedido.tipo = TipoDePedido.objects.get(id=1)
            pedido.assunto = assunto
            pedido.anoletivoid = ano_letivo.objects.get(ativo="S")
            pedido.informacoes = descricao 
            Horario.objects.filter(pedido_ptr_id=id).delete()

            if pedido.identificador_id.id == 2 and arquivo != "":
                ficheiros_dir = os.path.join(settings.BASE_DIR, 'ficheiros\pedido_') 
                ficheiros_dir = str(ficheiros_dir)+ str(id) + ".xls"
                os.remove(ficheiros_dir)
            elif pedido.identificador_id.id == 1:
                Horario.objects.filter(pedido_ptr_id=id).delete()

            pedido.identificador_id = IdentificadorPedido.objects.get(id=opcao)
            pedido.save()
            if opcao == "2" and arquivo != "":
                ficheiros_dir = os.path.join(settings.BASE_DIR, 'ficheiros')
                ficheiro_nome = f'pedido_{pedido.id}.{arquivo.name.split(".")[-1]}'
                with open(os.path.join(ficheiros_dir, ficheiro_nome), 'wb') as f:
                    for chunk in arquivo.chunks():
                        f.write(chunk)
            elif opcao == "1":
                Horario.objects.filter(pedido_ptr_id=id).delete()
                for subpedido in subpedidos:
                    if (subpedido['acoes'] == "alterar"):
                        horario = Horario(acao = subpedido['acoes'],
                                          data_h=subpedido['date_h'],
                                          hora_inicial=subpedido['timeinicial'],
                                          hora_final=subpedido['timefinal'],
                                          descricao=subpedido['descricao'],
                                          pedido_ptr_id=pedido.id)
                    else:
                        horario = Horario(acao = subpedido['acoes'],
                                          data_h=subpedido['date_h'],
                                          hora_inicial=subpedido['timeinicial'],
                                          hora_final=subpedido['timefinal'],
                                          descricao=subpedido['descricao'],
                                          pedido_ptr_id=pedido.id)
                    horario.save()
            return redirect('main:mensagem',5)
    else:
        pedidoid = id
        pedido = Pedido.objects.get(id=pedidoid)
        data_alvo = str(pedido.data_de_alvo)
        data_objeto = parser.parse(data_alvo)
        data_formatada = data_objeto.strftime('%Y-%m-%d')
        pedido = Pedido.objects.get(id=id)
        identificador = pedido.identificador_id.id
        subpedidos = []
        file_url = ""
        if identificador == 1:
            horario = Horario.objects.filter(pedido_ptr_id=id)
            for horarios in horario:
                subpedido = {}
                subpedido['acoes'] = horarios.acao
                subpedido['date_h'] = horarios.data_h.strftime('%Y-%m-%d')
                subpedido['timeinicial'] = horarios.hora_inicial.strftime('%H:%M')
                subpedido['timefinal'] = horarios.hora_final.strftime('%H:%M')
                subpedido['descricao'] = horarios.descricao
                subpedidos.append(subpedido)
        elif identificador == 2:
            pedido_ficheiro_nome = "pedido_" + str(pedido.id) + ".xls"
            file_url = os.path.join(settings.BASE_DIR, 'ficheiros', pedido_ficheiro_nome)        
        form = PedidoHorarioForm(initial={'descricao': pedido.informacoes,'data':data_formatada, 'assunto': pedido.assunto})
        msg = ""
        return render(request, 
                  template_name="pedido/editar_pedido_horario.html",
                  context={'erros': erros,'msg':msg,'form':form, 'pedidos':subpedidos, 'tipo': identificador, 'file_url': file_url})



def consultar_pedido_horario(request, id):
    pedido = Pedido.objects.get(id=id)
    pedido.estado = pedido.estado_0.estado
    pedido.data_de_alvo = pedido.data_de_alvo.strftime('%d/%m/%Y')
    file_url = ""
    if pedido.identificador_id.id == 1:
        horario = Horario.objects.filter(pedido_ptr_id=pedido.id)
        subpedidos = []
        for horarios in horario:
            subpedido = {}
            subpedido['acoes'] = horarios.acao
            subpedido['date_h'] = horarios.data_h.strftime('%Y-%m-%d')
            subpedido['timeinicial'] = horarios.hora_inicial.strftime('%H:%M')
            subpedido['timefinal'] = horarios.hora_final.strftime('%H:%M')
            subpedido['descricao'] = horarios.descricao
            subpedidos.append(subpedido)
        pedido.subpedidos = subpedidos
    else:
        pedido_ficheiro_nome = "pedido_" + str(pedido.id) + ".xls"
        file_url = os.path.join(settings.BASE_DIR, 'ficheiros', pedido_ficheiro_nome)     
        pedido.fire_url = file_url
    return render(request, 
                 'pedido/consultar_pedido_horario.html', 
                  context={'pedido_horario': pedido, 'file_url': file_url})
    

def eliminar_pedido_horario(request, id):
    pedido = Pedido.objects.get(id=id)
    user = get_user(request)
    if user.groups.filter(name = "Docente").exists():
        if pedido.estado_0.estado == 'Pendente':
            if request.method == 'POST':
                if 'confirmar' in request.POST:
                    if pedido.identificador_id.id == 1:
                        Horario.objects.filter(pedido_ptr_id=id).delete()
                    else:
                        ficheiros_dir = os.path.join(settings.BASE_DIR, 'ficheiros\pedido_') 
                        ficheiros_dir = str(ficheiros_dir)+ str(id) + ".xls"
                        os.remove(ficheiros_dir)
                    pedido.delete()
                    return redirect('main:mensagem',6)
                else:
                    return redirect('main:listar-pedidos')
            else:
                return render(request, 'pedido/eliminar_pedido_horario.html', {'pedido_id': id})
        else:
            return redirect('main:mensagem',7)
    elif user.groups.filter(name = "Funcionario").exists():
        return redirect('main:mensagem',8)





####################################################################################################################
################### Incicio de criar Pedido Sala                 ####################################3333
####################################################################################################################



def criar_pedidos_sala(request):
    erros = ""
    msg = ""
    user = get_user(request)
    salas = Sala.objects.filter(id_ano_letivo=ano_letivo.objects.get(ativo="S").id).all()
    salas_t = []
    for s in salas:
        sala = {};
        sala['id'] = s.id;
        sala['lotacao'] = s.lotacao;
        sala['descricao_sala'] = s.descricao_sala;
        sala['id_nome_instituicao'] = s.id_nome_instituicao;
        sala['id_nome_edificio'] = s.id_nome_edificio;
        sala['id_nome_tipo_sala'] = s.id_nome_tipo_sala;
        sala['id_nome_edificio'] = s.id_nome_edificio;
        sala['id_ano_letivo'] = s.id_ano_letivo;
        sala['id_estado_da_sala'] = s.id_estado_da_sala;
        sala['id_tipo_de_sala'] = s.id_tipo_aula;
        sala['tipo_de_sala'] = TipoDeAulas.objects.get(id=s.id_tipo_aula).tipo_aula;
        sala['nome_instituicao'] = Instituicao.objects.get(id=s.id_nome_instituicao).nome_instituicao;
        sala['nome_edificio'] =  Edificio.objects.get(id=s.id_nome_edificio).edificio;
        sala['nome_tipo_sala'] = Categoria.objects.get(id=s.id_tipo_aula).tipo_de_sala;
        sala['ano_letivo'] =  ano_letivo.objects.get(id=s.id_ano_letivo).ano_letivo;
        sala['estado_da_sala'] = EstadoSala.objects.get(id=s.id_estado_da_sala).estado;
        salas_t.append(sala);

    edificios=Edificio.objects.all()
    edificios_t =[]
    for e in edificios:
                edificio={};
                edificio['id'] = e.id;
                edificio['edificio'] = e.edificio;
                edificios_t.append(edificio);
                
    instituicao=Instituicao.objects.all()
    instituicao_t =[]
    for i in instituicao:
                instituicao={};
                instituicao['id'] = i.id;
                instituicao['nome_instituicao'] = i.nome_instituicao;
                instituicao_t.append(instituicao);

    tipodeaula=TipoDeAulas.objects.all()
    tipodeaula_t =[]
    for t in tipodeaula:
                tipodeaula={};
                tipodeaula['id'] = t.id;
                tipodeaula['tipo_aula'] = t.tipo_aula;
                tipodeaula_t.append(tipodeaula);

    categoria=Categoria.objects.all()
    categoria_t =[]
    for d in categoria:
                categoria={};
                categoria['id'] = d.id;
                categoria['tipo_de_sala'] = d.tipo_de_sala;
                categoria_t.append(categoria);

    
    if user.groups.filter(name = "Docente").exists():
        if request.method == 'POST':
            subpedidos = json.loads(request.POST['subpedidos'])
            form = PedidoSalasForm(request.POST)
            descricao = request.POST.get('informacoes', '')
            assunto = request.POST.get('assunto', '')
            data = request.POST.get('data', '')
             #Verificação da data
            try:
                data = datetime.datetime.strptime(data, '%Y-%m-%d').date()
                hoje = datetime.date.today()
                data_destino =  ano_letivo.objects.get(ativo="S").dia_fim
                if data < hoje or data > data_destino:
                    erros = "A data deve estar entre hoje e fim do ano letivo( "+ str(data_destino) + ")";
                    msg = True
                    return render(request, 
                        template_name="pedido/criar_pedido_sala.html",
                        context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos,'salass':salas_t,'edificios':edificios_t,'instituicoes':instituicao_t,'tipodeaulas':tipodeaula_t,'categorias':categoria_t})
            except ValueError:
                erros = "Data inválida."
                msg = True
                return render(request, 
                    template_name="pedido/criar_pedido_sala.html",
                    context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos,'salass':salas_t,'edificios':edificios_t,'instituicoes':instituicao_t,'tipodeaulas':tipodeaula_t,'categorias':categoria_t})



            #Verificação do assunto
            if len(assunto) < 5:
                erros = "Assunto têm de ter mais que 5 caracteres."
                msg = True
                return render(request, 
                    template_name="pedido/criar_pedido_sala.html",
                    context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos,'salass':salas_t,'edificios':edificios_t,'instituicoes':instituicao_t,'tipodeaulas':tipodeaula_t,'categorias':categoria_t})

            #Verificação da descricao geral
            elif len(descricao) < 5:
                erros = "Informações têm de ter mais que 5 caracteres."
                msg = True
                return render(request, 
                    template_name="pedido/criar_pedido_sala.html",
                    context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos,'salass':salas_t,'edificios':edificios_t,'instituicoes':instituicao_t,'tipodeaulas':tipodeaula_t,'categorias':categoria_t})
            elif(subpedidos == []):
                    erros = "Têm que haver pelo menos um subpedido"
                    msg = True
                    return render(request, 
                        template_name="pedido/criar_pedido_sala.html",
                        context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos,'salass':salas_t,'edificios':edificios_t,'instituicoes':instituicao_t,'tipodeaulas':tipodeaula_t,'categorias':categoria_t})

            if form.is_valid():
                #Verificacao se existe duplicação de Pedidos na BD
                try:
                    PedidoDeSala.objects.get(docenteutilizadorid=request.user.id, data_de_alvo=data, assunto=assunto)
                    erros = "Já existe um pedido com esta data e assunto."
                    msg = True
                    return render(request, template_name="pedido/criar_pedido_sala.html",
                        context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos,'salass':salas_t,'edificios':edificios_t,'instituicoes':instituicao_t,'tipodeaulas':tipodeaula_t,'categorias':categoria_t})


                except ObjectDoesNotExist:
                    pedido = form.save(commit=False)
                    pedido.estado_0 = EstadoPedido.objects.get(id=1)
                    pedido.docenteutilizadorid = Docente.objects.get(utilizador_ptr_id=request.user.id)
                    pedido.data_de_submissao = datetime.date.today()
                    pedido.data_de_alvo = data
                    pedido.tipo = TipoDePedido.objects.get(id=3)
                    pedido.assunto = assunto
                    pedido.anoletivoid = ano_letivo.objects.get(ativo="S")
                    pedido.informacoes = descricao 
                    pedido.save()
                    for subpedido in subpedidos:
                        print(subpedido)

                        
                        if(subpedido['sala_especifica'] == "" and subpedido['action'] == "3" ):
                           print("if1")
                           Subpedido_sala = subpedido_sala(
                                        descricao=subpedido['descricao'],  #numeros azul do models subpedidos
                                        inicio=subpedido['inicio'],
                                        fim=subpedido['fim'],
                                        id_instituicao  = subpedido['instituicao'],
                                        id_edificio =  subpedido['edificio'],
                                        categoria = subpedido['tipo_sala'],
                                        id_tipo_de_aula = subpedido['tipodeaula'],
                                        numero_alunos =  subpedido['numero_alunos'],
                                        acao = subpedido['action'],
                                        pedido_ptr_id=PedidoDeSala.objects.get(pedido_ptr_id=pedido.id).id,
                                        editar_descricao=subpedido['editar_descricao'],
                                        editar_inicio=subpedido['editar_inicio'],
                                        editar_fim=subpedido['editar_fim'],
                                        editar_id_instituicao  = subpedido['editar_instituicao'],
                                        editar_id_edificio =  subpedido['editar_edificio'],
                                        editar_categoria = subpedido['editar_tipo_sala'],
                                        editar_id_tipo_de_aula = subpedido['editar_tipodeaula'],
                                        editar_numero_alunos =  subpedido['editar_numero_alunos'],
                                        )
                        elif(subpedido['sala_especifica'] == ""):
                            print("if2")
                            Subpedido_sala = subpedido_sala(
                                        descricao=subpedido['descricao'],  #numeros azul do models subpedidos
                                        inicio=subpedido['inicio'],
                                        fim=subpedido['fim'],
                                        id_instituicao  = subpedido['instituicao'],
                                        id_edificio =  subpedido['edificio'],
                                        categoria = subpedido['tipo_sala'],
                                        id_tipo_de_aula = subpedido['tipodeaula'],
                                        numero_alunos =  subpedido['numero_alunos'],
                                        acao = subpedido['action'],
                                        pedido_ptr_id=PedidoDeSala.objects.get(pedido_ptr_id=pedido.id).id,
                                        )
                        elif(subpedido['action'] == "3" ):
                            print("if3")
                            Subpedido_sala = subpedido_sala(
                                        descricao=subpedido['descricao'],
                                        inicio=subpedido['inicio'],
                                        fim=subpedido['fim'],
                                        acao = subpedido['action'],
                                        id_sala = subpedido['sala_especifica'],
                                        pedido_ptr_id=PedidoDeSala.objects.get(pedido_ptr_id=pedido.id).id,
                                        editar_descricao=subpedido['editar_descricao'],
                                        editar_inicio=subpedido['editar_inicio'],
                                        editar_fim=subpedido['editar_fim'],
                                        editar_id_sala = subpedido['editar_sala_especifica'],
                                        )                         
                        else:
                            print("if4")
                            Subpedido_sala = subpedido_sala(
                                        descricao=subpedido['descricao'],
                                        inicio=subpedido['inicio'],
                                        fim=subpedido['fim'],
                                        acao = subpedido['action'],
                                        id_sala = subpedido['sala_especifica'],
                                        pedido_ptr_id=PedidoDeSala.objects.get(pedido_ptr_id=pedido.id).id,
                                        )    

                        

                        Subpedido_sala.save()
                    return redirect('main:mensagem',4)

        else:
            form = PedidoSalasForm()
            msg = False



                


    

        return render(request, 
                    template_name="pedido/criar_pedido_sala.html",
                    context={'erros': erros,'msg':msg,'form':form,'salass':salas_t,'edificios':edificios_t,'instituicoes':instituicao_t,'tipodeaulas':tipodeaula_t,'categorias':categoria_t})



####################################################################################################################
################### Fim de criar Pedido Sala                 ####################################3333
####################################################################################################################


####################################################################################################################
################### Incicio de Editar Pedido Sala                 ####################################3333
####################################################################################################################



def editar_pedido_sala(request,id):
    erros = ""
    user = get_user(request)
    salas = Sala.objects.filter(id_ano_letivo=ano_letivo.objects.get(ativo="S").id).all()
    salas_t = []
    for s in salas:
        sala = {};
        sala['id'] = s.id;
        sala['lotacao'] = s.lotacao;
        sala['descricao_sala'] = s.descricao_sala;
        sala['id_nome_instituicao'] = s.id_nome_instituicao;
        sala['id_nome_edificio'] = s.id_nome_edificio;
        sala['id_nome_tipo_sala'] = s.id_nome_tipo_sala;
        sala['id_nome_edificio'] = s.id_nome_edificio;
        sala['id_ano_letivo'] = s.id_ano_letivo;
        sala['id_estado_da_sala'] = s.id_estado_da_sala;
        sala['id_tipo_de_sala'] = s.id_tipo_aula;
        sala['tipo_de_sala'] = TipoDeAulas.objects.get(id=s.id_tipo_aula).tipo_aula;
        sala['nome_instituicao'] = Instituicao.objects.get(id=s.id_nome_instituicao).nome_instituicao;
        sala['nome_edificio'] =  Edificio.objects.get(id=s.id_nome_edificio).edificio;
        sala['nome_tipo_sala'] = Categoria.objects.get(id=s.id_tipo_aula).tipo_de_sala;
        sala['ano_letivo'] =  ano_letivo.objects.get(id=s.id_ano_letivo).ano_letivo;
        sala['estado_da_sala'] = EstadoSala.objects.get(id=s.id_estado_da_sala).estado;
        salas_t.append(sala);

    edificios=Edificio.objects.all()
    edificios_t =[]
    for e in edificios:
                edificio={};
                edificio['id'] = e.id;
                edificio['edificio'] = e.edificio;
                edificios_t.append(edificio);
                
    instituicao=Instituicao.objects.all()
    instituicao_t =[]
    for i in instituicao:
                instituicao={};
                instituicao['id'] = i.id;
                instituicao['nome_instituicao'] = i.nome_instituicao;
                instituicao_t.append(instituicao);

    tipodeaula=TipoDeAulas.objects.all()
    tipodeaula_t =[]
    for t in tipodeaula:
                tipodeaula={};
                tipodeaula['id'] = t.id;
                tipodeaula['tipo_aula'] = t.tipo_aula;
                tipodeaula_t.append(tipodeaula);

    categoria=Categoria.objects.all()
    categoria_t =[]
    for d in categoria:
                categoria={};
                categoria['id'] = d.id;
                categoria['tipo_de_sala'] = d.tipo_de_sala;
                categoria_t.append(categoria);

    if request.method == 'POST':
            subpedidos = json.loads(request.POST['subpedidos'])
            form = PedidoSalasForm(request.POST)
            descricao = request.POST.get('informacoes', '')
            assunto = request.POST.get('assunto', '')
            data = request.POST.get('data', '')

             #Verificação da data
            try:
                data = datetime.datetime.strptime(data, '%Y-%m-%d').date()
                hoje = datetime.date.today()
                data_destino =  ano_letivo.objects.get(ativo="S").dia_fim
                if data < hoje or data > data_destino:
                    erros = "A data deve estar entre hoje e fim do ano letivo( "+ str(data_destino) + ")";
                    msg = True
                    return render(request, 
                        template_name="pedido/editar_pedido_sala.html",
                        context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos,'salass':salas_t,'edificios':edificios_t,'instituicoes':instituicao_t,'tipodeaulas':tipodeaula_t,'categorias':categoria_t,'fase':False})
            except ValueError:
                erros = "Data inválida."
                msg = True
                return render(request, 
                    template_name="pedido/editar_pedido_sala.html",
                    context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos,'salass':salas_t,'edificios':edificios_t,'instituicoes':instituicao_t,'tipodeaulas':tipodeaula_t,'categorias':categoria_t,'fase':False})



            #Verificação do assunto
            if len(assunto) < 5:
                erros = "Assunto têm de ter mais que 5 caracteres."
                msg = True
                return render(request, 
                    template_name="pedido/editar_pedido_sala.html",
                    context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos,'salass':salas_t,'edificios':edificios_t,'instituicoes':instituicao_t,'tipodeaulas':tipodeaula_t,'categorias':categoria_t,'fase':False})

            #Verificação da descricao geral
            elif len(descricao) < 5:
                erros = "Informações têm de ter mais que 5 caracteres."
                msg = True
                return render(request, 
                    template_name="pedido/editar_pedido_sala.html",
                    context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos,'salass':salas_t,'edificios':edificios_t,'instituicoes':instituicao_t,'tipodeaulas':tipodeaula_t,'categorias':categoria_t,'fase':False})

            elif(subpedidos == []):
                    erros = "Têm que haver pelo menos um subpedido"
                    msg = True
                    return render(request, 
                    template_name="pedido/editar_pedido_sala.html",
                    context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos,'salass':salas_t,'edificios':edificios_t,'instituicoes':instituicao_t,'tipodeaulas':tipodeaula_t,'categorias':categoria_t,'fase':False})


                
            if form.is_valid():   
                pedido = PedidoDeSala.objects.get(id=id) 
                pedido.estado_0 = EstadoPedido.objects.get(id=1)
                pedido.docenteutilizadorid = Docente.objects.get(utilizador_ptr_id=request.user.id)
                pedido.data_de_submissao = datetime.date.today()
                pedido.data_de_alvo = data
                pedido.tipo = TipoDePedido.objects.get(id=3)
                pedido.assunto = assunto
                pedido.anoletivoid = ano_letivo.objects.get(ativo="S")
                pedido.informacoes = descricao 
                pedido.save()   
                subpedido_sala.objects.filter(pedido_ptr_id=id).delete()
                for subpedido in subpedidos:
                        
                        if(subpedido['sala_especifica'] == "" and subpedido['action'] == "3" ):
                           print("if1")
                           print(subpedido)
                           Subpedido_sala = subpedido_sala(
                                        descricao=subpedido['descricao'],  #numeros azul do models subpedidos
                                        inicio=subpedido['inicio'],
                                        fim=subpedido['fim'],
                                        id_instituicao  = subpedido['instituicao'],
                                        id_edificio =  subpedido['edificio'],
                                        categoria = subpedido['tipo_sala'],
                                        id_tipo_de_aula = subpedido['tipodeaula'],
                                        numero_alunos =  subpedido['numero_alunos'],
                                        acao = subpedido['action'],
                                        pedido_ptr_id=PedidoDeSala.objects.get(pedido_ptr_id=pedido.id).id,
                                        editar_descricao=subpedido['editar_descricao'],
                                        editar_inicio=subpedido['editar_inicio'],
                                        editar_fim=subpedido['editar_fim'],
                                        editar_id_instituicao  = subpedido['editar_instituicao'],
                                        editar_id_edificio =  subpedido['editar_edificio'],
                                        editar_categoria = subpedido['editar_tipo_sala'],
                                        editar_id_tipo_de_aula = subpedido['editar_tipodeaula'],
                                        editar_numero_alunos =  subpedido['editar_numero_alunos'],
                                        )
                        elif(subpedido['sala_especifica'] == ""):
                            print("if2")
                            print(subpedido)
                            Subpedido_sala = subpedido_sala(
                                        descricao=subpedido['descricao'],  #numeros azul do models subpedidos
                                        inicio=subpedido['inicio'],
                                        fim=subpedido['fim'],
                                        id_instituicao  = subpedido['instituicao'],
                                        id_edificio =  subpedido['edificio'],
                                        categoria = subpedido['tipo_sala'],
                                        id_tipo_de_aula = subpedido['tipodeaula'],
                                        numero_alunos =  subpedido['numero_alunos'],
                                        acao = subpedido['action'],
                                        pedido_ptr_id=PedidoDeSala.objects.get(pedido_ptr_id=pedido.id).id,
                                        )
                        elif(subpedido['action'] == "3" ):
                            print("if3")
                            print(subpedido)
                            Subpedido_sala = subpedido_sala(
                                        descricao=subpedido['descricao'],
                                        inicio=subpedido['inicio'],
                                        fim=subpedido['fim'],
                                        acao = subpedido['action'],
                                        id_sala = subpedido['sala_especifica'],
                                        pedido_ptr_id=PedidoDeSala.objects.get(pedido_ptr_id=pedido.id).id,
                                        editar_descricao=subpedido['editar_descricao'],
                                        editar_inicio=subpedido['editar_inicio'],
                                        editar_fim=subpedido['editar_fim'],
                                        editar_id_sala = subpedido['editar_sala_especifica'],
                                        )                         
                        else:
                            print("if4")
                            print(subpedido)
                            Subpedido_sala = subpedido_sala(
                                        descricao=subpedido['descricao'],
                                        inicio=subpedido['inicio'],
                                        fim=subpedido['fim'],
                                        acao = subpedido['action'],
                                        id_sala = subpedido['sala_especifica'],
                                        pedido_ptr_id=PedidoDeSala.objects.get(pedido_ptr_id=pedido.id).id,
                                        )    

                        

                        Subpedido_sala.save()
                return redirect('main:mensagem',5)
    else:
        pedidoid = id
        pedido = Pedido.objects.get(id=pedidoid)
        data_alvo = str(pedido.data_de_alvo)
        data_objeto = parser.parse(data_alvo)
        data_formatada = data_objeto.strftime('%Y-%m-%d')
        pedido = Pedido.objects.get(id=id)
        salas = subpedido_sala.objects.filter(pedido_ptr_id=id)
        subpedidos =[]
        for sala in salas:
            subpedido = {}

            
            if(sala.acao == 3 and sala.numero_alunos is None):
                subpedido['numero_alunos'] = 0
                subpedido['descricao'] = sala.descricao
                subpedido['sala_especifica'] = Sala.objects.get(id=sala.id_sala).id
                subpedido['action'] = sala.acao
                subpedido['editar_descricao'] = sala.editar_descricao                
                subpedido['inicio'] = sala.inicio
                subpedido['editar_inicio'] = sala.editar_inicio
                subpedido['fim'] = sala.fim
                subpedido['editar_fim'] = sala.editar_fim
                subpedido['editar_sala_especifica'] = Sala.objects.get(id=sala.editar_id_sala).id
                subpedido['Salaespecifica_name'] = Sala.objects.get(id=sala.id_sala).descricao_sala
                subpedido['editar_Salaespecifica_name'] = Sala.objects.get(id=sala.editar_id_sala).descricao_sala

            elif(sala.acao == 3):
                subpedido['numero_alunos'] = sala.numero_alunos
                subpedido['descricao'] = sala.descricao
                subpedido['sala_especifica'] = ""                
                subpedido['tipo_sala'] = Categoria.objects.get(id=sala.categoria).id
                subpedido['instituicao'] = Instituicao.objects.get(id=sala.id_instituicao).id
                subpedido['tipodeaula'] = TipoDeAulas.objects.get(id=sala.id_tipo_de_aula).id
                subpedido['edificio'] = Edificio.objects.get(id=sala.id_edificio).id
                subpedido['inicio'] = sala.inicio
                subpedido['fim'] = sala.fim
                subpedido['action'] = sala.acao 
                subpedido['edificio_name'] = Edificio.objects.get(id=sala.id_edificio).edificio
                subpedido['instituicao_name'] = Instituicao.objects.get(id=sala.id_instituicao).nome_instituicao
                subpedido['tipodeaula_name'] = TipoDeAulas.objects.get(id=sala.id_tipo_de_aula).tipo_aula
                subpedido['tipo_sala_name'] = Categoria.objects.get(id=sala.categoria).tipo_de_sala
                subpedido['editar_numero_alunos'] = sala.editar_numero_alunos
                subpedido['editar_descricao'] = sala.editar_descricao                
                subpedido['editar_sala_especifica'] = ""                
                subpedido['editar_instituicao'] = Instituicao.objects.get(id=sala.editar_id_instituicao).id
                subpedido['editar_tipodeaula'] = TipoDeAulas.objects.get(id=sala.editar_id_tipo_de_aula).id   
                subpedido['editar_edificio'] = Edificio.objects.get(id=sala.editar_id_edificio).id
                subpedido['editar_inicio'] = sala.editar_inicio
                subpedido['editar_fim'] = sala.editar_fim                
                subpedido['editar_edificio_name'] = Edificio.objects.get(id=sala.editar_id_edificio).edificio
                subpedido['editar_instituicao_name'] = Instituicao.objects.get(id=sala.editar_id_instituicao).nome_instituicao                
                subpedido['editar_tipodeaula_name'] = TipoDeAulas.objects.get(id=sala.editar_id_tipo_de_aula).tipo_aula 
                subpedido['editar_tipo_sala_name'] = Categoria.objects.get(id=sala.editar_categoria).tipo_de_sala
                subpedido['editar_tiposala'] = Categoria.objects.get(id=sala.editar_categoria).id   

  
            elif(sala.numero_alunos is None):
                subpedido ={
                    'numero_alunos': 0,
                    'descricao': sala.descricao ,
                    'sala_especifica':Sala.objects.get(id=sala.id_sala).id,
                    'Salaespecifica_name':Sala.objects.get(id=sala.id_sala).descricao_sala,
                    'action': sala.acao,
                    'inicio':sala.inicio,
                    'fim':sala.fim
                }
            else:
                subpedido['numero_alunos'] = sala.numero_alunos
                subpedido['descricao'] = sala.descricao           
                subpedido['sala_especifica'] = ""
                subpedido['tipo_sala'] = Categoria.objects.get(id=sala.categoria).id
                subpedido['instituicao'] = Instituicao.objects.get(id=sala.id_instituicao).id
                subpedido['tipodeaula'] = TipoDeAulas.objects.get(id=sala.id_tipo_de_aula).id
                subpedido['edificio'] = Edificio.objects.get(id=sala.id_edificio).id
                subpedido['inicio'] = sala.inicio
                subpedido['fim'] = sala.fim
                subpedido['action'] = sala.acao 
                subpedido['edificio_name'] = Edificio.objects.get(id=sala.id_edificio).edificio
                subpedido['instituicao_name'] = Instituicao.objects.get(id=sala.id_instituicao).nome_instituicao
                subpedido['tipodeaula_name'] = TipoDeAulas.objects.get(id=sala.id_tipo_de_aula).tipo_aula
                subpedido['tipo_sala_name'] = Categoria.objects.get(id=sala.categoria).tipo_de_sala



            subpedidos.append(subpedido) 
        form = PedidoSalasForm(initial={'informacoes': pedido.informacoes,'data':data_formatada, 'assunto': pedido.assunto})
    msg = ""
    return render(request, 
                  template_name="pedido/editar_pedido_sala.html",
                  context={'erros': erros,'msg':msg,'form':form,'pedidos':subpedidos,'salass':salas_t,'edificios':edificios_t,'instituicoes':instituicao_t,'tipodeaulas':tipodeaula_t,'categorias':categoria_t,'fase':True})


          
####################################################################################################################
################### Fim de Editar Pedido Sala                 ####################################3333
####################################################################################################################


####################################################################################################################
################### Incicio de Eliminar Pedido Sala                 ####################################3333
####################################################################################################################

def eliminar_pedido_sala(request, id):
    pedido = Pedido.objects.get(id=id)
    user = get_user(request)
    if user.groups.filter(name = "Docente").exists():
        if pedido.estado_0.estado == 'Pendente':
            if request.method == 'POST':
                if 'confirmar' in request.POST:
                    subpedido_sala.objects.filter(pedido_ptr_id=id).delete()
                    pedido.delete()
                    return redirect('main:mensagem',6)
                else:
                    return redirect('pedidos:listagem-pedidos')
            else:
                return render(request, 'pedido/eliminar_pedido_outros.html', {'pedido_id': id})
        else:
            return redirect('main:mensagem',7)
    elif user.groups.filter(name = "Funcionario").exists():
        return redirect('main:mensagem',8)

####################################################################################################################
################### Fim de Eliminar Pedido Sala                 ####################################3333
####################################################################################################################



####################################################################################################################
################### Incicio de Consultar Pedido Sala                 ####################################3333
####################################################################################################################

def consultar_pedido_sala(request,id):
    pedido = Pedido.objects.get(id=id);
    salas = subpedido_sala.objects.filter(pedido_ptr_id=pedido.id)
    pedido.data_de_alvo = pedido.data_de_alvo.strftime('%d/%m/%Y');
    subpedidos = []
    for sala in salas:
        subpedido = {}

        if(sala.acao == 3 and sala.numero_alunos is None):
            subpedido['descricao'] = sala.descricao
            subpedido['editar_descricao'] = sala.editar_descricao                
            subpedido['inicio'] = sala.inicio
            subpedido['editar_inicio'] = sala.editar_inicio
            subpedido['fim'] = sala.fim
            subpedido['editar_fim'] = sala.editar_fim
            subpedido['action'] = sala.acao
            subpedido['sala_especifica'] = Sala.objects.get(id=sala.id_sala).descricao_sala
            subpedido['editar_sala_especifica'] = Sala.objects.get(id=sala.editar_id_sala).descricao_sala
            subpedido['numero_alunos'] = 0
        elif(sala.acao == 3):
            subpedido['sala_especifica'] = ""
            subpedido['descricao'] = sala.descricao
            subpedido['editar_descricao'] = sala.editar_descricao                
            subpedido['inicio'] = sala.inicio
            subpedido['editar_inicio'] = sala.editar_inicio
            subpedido['fim'] = sala.fim
            subpedido['editar_fim'] = sala.editar_fim
            subpedido['instituicao'] = Instituicao.objects.get(id=sala.id_instituicao).nome_instituicao
            subpedido['editar_instituicao'] = Instituicao.objects.get(id=sala.editar_id_instituicao).nome_instituicao
            subpedido['edificio'] = Edificio.objects.get(id=sala.id_edificio).edificio
            subpedido['editar_edificio'] = Edificio.objects.get(id=sala.editar_id_edificio).edificio
            subpedido['tipo_sala'] = Categoria.objects.get(id=sala.categoria).tipo_de_sala
            subpedido['editar_tipo_sala'] = Categoria.objects.get(id=sala.editar_categoria).tipo_de_sala
            subpedido['tipodeaula'] = TipoDeAulas.objects.get(id=sala.id_tipo_de_aula).tipo_aula
            subpedido['editar_tipodeaula'] = TipoDeAulas.objects.get(id=sala.editar_id_tipo_de_aula).tipo_aula   
            subpedido['numero_alunos'] = sala.numero_alunos
            subpedido['editar_numero_alunos'] = sala.editar_numero_alunos
            subpedido['action'] = sala.acao 
        elif(sala.numero_alunos is None):
            subpedido['descricao'] = sala.descricao              
            subpedido['inicio'] = sala.inicio
            subpedido['fim'] = sala.fim
            subpedido['action'] = sala.acao
            subpedido['sala_especifica'] = Sala.objects.get(id=sala.id_sala).descricao_sala
            subpedido['numero_alunos'] = 0
        else:
            subpedido['sala_especifica'] = ""
            subpedido['descricao'] = sala.descricao           
            subpedido['inicio'] = sala.inicio
            subpedido['fim'] = sala.fim
            subpedido['instituicao'] = Instituicao.objects.get(id=sala.id_instituicao).nome_instituicao
            subpedido['edificio'] = Edificio.objects.get(id=sala.id_edificio).edificio
            subpedido['tipo_sala'] = Categoria.objects.get(id=sala.categoria).tipo_de_sala
            subpedido['tipodeaula'] = TipoDeAulas.objects.get(id=sala.id_tipo_de_aula).tipo_aula
            subpedido['numero_alunos'] = sala.numero_alunos
            subpedido['action'] = sala.acao 


                    
                                    
                
        subpedidos.append(subpedido)
    pedido.subpedidos = subpedidos
    return render(request, 
                        'pedido/consultar_pedido_sala.html',
                        context={'pedido_sala': pedido})


####################################################################################################################
################### Fim de Consultar Pedido Sala                 ####################################3333
####################################################################################################################

def sendNot(FROM, password, TO, subject, message):
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = subject
    msg['From'] = FROM
    msg['To'] = TO
    server = smtplib.SMTP( 'smtp.office365.com', 587 )
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(FROM, password)
    server.send_message(msg)
    return

def validar_pedido(request,id):
    if request.method == 'POST':
        acao_selecionada = request.POST.get('acao')
        comments = request.POST.get('comentarios')
        pedido = Pedido.objects.get(id=id)
        pedido.comentarios = comments
        pedido.data_de_validacao = datetime.datetime.today()
        if acao_selecionada == 'A':
            pedido.estado_0 = EstadoPedido.objects.get(id=3)
        elif acao_selecionada == 'R':
            pedido.estado_0 = EstadoPedido.objects.get(id=4)
        pedido.save()
        user = get_user(request)
        userEmail = 'funcionario_funcionario@outlook.com'
        docenteEmail = AuthUser.objects.get(id=pedido.docenteutilizadorid.utilizador_ptr_id).email
        message = comments
        if pedido.tipo.id == 1:
            message += '\n' + 'http://127.0.0.1:8000/consultarpedidohorario/' + str(id)
        elif pedido.tipo.id == 2:
            message += '\n' + 'http://127.0.0.1:8000/consultarpedidooutros/' + str(id)
        elif pedido.tipo.id == 3:
            message += '\n' + 'http://127.0.0.1:8000/consultarpedidosala/' + str(id)
        elif pedido.tipo.id == 4:
            message += '\n' + 'http://127.0.0.1:8000/consultarpedidosuc/' + str(id)
        sendNot(userEmail, 'Funcionario', docenteEmail, 'Validacao pedido ' + str(pedido.id), message)
        return redirect('main:mensagem',15)
    else:
        pedido = Pedido.objects.get(id=id)
        horario = Horario.objects.filter(pedido_ptr_id=pedido.id)
        pedido.data_de_alvo = pedido.data_de_alvo.strftime('%d/%m/%Y')
        subpedidos = []
        if pedido.tipo.id == 1:
            for horarios in horario:
                subpedido = {}
                subpedido['acoes'] = horarios.acao
                subpedido['date_h'] = horarios.data_h.strftime('%Y-%m-%d')
                subpedido['timeinicial'] = horarios.hora_inicial.strftime('%H:%M')
                subpedido['timefinal'] = horarios.hora_final.strftime('%H:%M')
                subpedido['descricao'] = horarios.descricao
                subpedidos.append(subpedido)
        elif pedido.tipo.id == 2:
            outros = Outros.objects.filter(pedido_ptr_id=pedido.id)
            for outro in outros:
                subpedido = {}
                subpedido['assunto'] = outro.Assunto
                subpedido['descricao'] = outro.Descricao
                subpedidos.append(subpedido)
        elif pedido.tipo.id == 3:
            salas = subpedido_sala.objects.filter(pedido_ptr_id=pedido.id)
            for sala in salas:
                subpedido = {}           
                if(sala.acao == 3 and sala.numero_alunos is None):
                    subpedido['descricao'] = sala.descricao
                    subpedido['editar_descricao'] = sala.editar_descricao                
                    subpedido['inicio'] = sala.inicio
                    subpedido['editar_inicio'] = sala.editar_inicio
                    subpedido['fim'] = sala.fim
                    subpedido['editar_fim'] = sala.editar_fim
                    subpedido['action'] = sala.acao
                    subpedido['sala_especifica'] = Sala.objects.get(id=sala.id_sala).descricao_sala
                    subpedido['editar_sala_especifica'] = Sala.objects.get(id=sala.editar_id_sala).descricao_sala
                    subpedido['numero_alunos'] = 0
                elif(sala.acao == 3):
                    subpedido['sala_especifica'] = ""
                    subpedido['descricao'] = sala.descricao
                    subpedido['editar_descricao'] = sala.editar_descricao                
                    subpedido['inicio'] = sala.inicio
                    subpedido['editar_inicio'] = sala.editar_inicio
                    subpedido['fim'] = sala.fim
                    subpedido['editar_fim'] = sala.editar_fim
                    subpedido['instituicao'] = Instituicao.objects.get(id=sala.id_instituicao).nome_instituicao
                    subpedido['editar_instituicao'] = Instituicao.objects.get(id=sala.editar_id_instituicao).nome_instituicao
                    subpedido['edificio'] = Edificio.objects.get(id=sala.id_edificio).edificio
                    subpedido['editar_edificio'] = Edificio.objects.get(id=sala.editar_id_edificio).edificio
                    subpedido['tipo_sala'] = Categoria.objects.get(id=sala.categoria).tipo_de_sala
                    subpedido['editar_tipo_sala'] = Categoria.objects.get(id=sala.editar_categoria).tipo_de_sala
                    subpedido['tipodeaula'] = TipoDeAulas.objects.get(id=sala.id_tipo_de_aula).tipo_aula
                    subpedido['editar_tipodeaula'] = TipoDeAulas.objects.get(id=sala.editar_id_tipo_de_aula).tipo_aula   
                    subpedido['numero_alunos'] = sala.numero_alunos
                    subpedido['editar_numero_alunos'] = sala.editar_numero_alunos
                    subpedido['action'] = sala.acao 
                elif(sala.numero_alunos is None):
                    subpedido['descricao'] = sala.descricao              
                    subpedido['inicio'] = sala.inicio
                    subpedido['fim'] = sala.fim
                    subpedido['action'] = sala.acao
                    subpedido['sala_especifica'] = Sala.objects.get(id=sala.id_sala).descricao_sala
                    subpedido['numero_alunos'] = 0
                else:
                    subpedido['sala_especifica'] = ""
                    subpedido['descricao'] = sala.descricao           
                    subpedido['inicio'] = sala.inicio
                    subpedido['fim'] = sala.fim
                    subpedido['instituicao'] = Instituicao.objects.get(id=sala.id_instituicao).nome_instituicao
                    subpedido['edificio'] = Edificio.objects.get(id=sala.id_edificio).edificio
                    subpedido['tipo_sala'] = Categoria.objects.get(id=sala.categoria).tipo_de_sala
                    subpedido['tipodeaula'] = TipoDeAulas.objects.get(id=sala.id_tipo_de_aula).tipo_aula
                    subpedido['numero_alunos'] = sala.numero_alunos
                    subpedido['action'] = sala.acao 
                subpedidos.append(subpedido)
        elif pedido.tipo.id == 4:
            uc = SubpedidoUc.objects.filter(pedido_ptr_id=pedido.id)
            for ucs in uc:
                subpedido = {}
                subpedido['acao'] = ucs.acao
                subpedido['uc'] = Uc.objects.get(id=ucs.ucid).disciplina
                subpedido['turma'] = ucs.turma
                subpedido['descricao'] = ucs.descricao
                subpedidos.append(subpedido)
        pedido.subpedidos = subpedidos
        return render(request, 
                        template_name="pedido/validar_pedido.html",
                        context={'pedido':pedido,})



def obter_informacao(request,id):
    if request.method == 'POST':
        pedido = Pedido.objects.get(id=id)
        comments = request.POST.get('comentarios')
        assunto = request.POST.get('assunto')
        user = get_user(request)
        userEmail = AuthUser.objects.get(id=user.id).email
        docenteEmail = 'a70882@ualg.pt'
        message = comments
        if pedido.tipo.id == 1:
            message += '\n' + 'http://127.0.0.1:8000/consultarpedidohorario/' + str(id)
        elif pedido.tipo.id == 2:
            message += '\n' + 'http://127.0.0.1:8000/consultarpedidooutros/' + str(id)
        elif pedido.tipo.id == 3:
            message += '\n' + 'http://127.0.0.1:8000/consultarpedidosala/' + str(id)
        elif pedido.tipo.id == 4:
            message += '\n' + 'http://127.0.0.1:8000/consultarpedidosuc/' + str(id)
        sendNot(userEmail, 'Funcionario', docenteEmail, assunto, message)
        return redirect('main:mensagem',25)
    else:
        pedido = Pedido.objects.get(id=id)
        horario = Horario.objects.filter(pedido_ptr_id=pedido.id)
        pedido.data_de_alvo = pedido.data_de_alvo.strftime('%d/%m/%Y')
        subpedidos = []
        if pedido.tipo.id == 1:
            for horarios in horario:
                subpedido = {}
                subpedido['acoes'] = horarios.acao
                subpedido['date_h'] = horarios.data_h.strftime('%Y-%m-%d')
                subpedido['timeinicial'] = horarios.hora_inicial.strftime('%H:%M')
                subpedido['timefinal'] = horarios.hora_final.strftime('%H:%M')
                subpedido['descricao'] = horarios.descricao
                subpedidos.append(subpedido)
        elif pedido.tipo.id == 2:
            outros = Outros.objects.filter(pedido_ptr_id=pedido.id)
            for outro in outros:
                subpedido = {}
                subpedido['assunto'] = outro.Assunto
                subpedido['descricao'] = outro.Descricao
                subpedidos.append(subpedido)
        elif pedido.tipo.id == 3:
            salas = subpedido_sala.objects.filter(pedido_ptr_id=pedido.id)
            for sala in salas:
                subpedido = {}           
                if(sala.acao == 3 and sala.numero_alunos is None):
                    subpedido['descricao'] = sala.descricao
                    subpedido['editar_descricao'] = sala.editar_descricao                
                    subpedido['inicio'] = sala.inicio
                    subpedido['editar_inicio'] = sala.editar_inicio
                    subpedido['fim'] = sala.fim
                    subpedido['editar_fim'] = sala.editar_fim
                    subpedido['action'] = sala.acao
                    subpedido['sala_especifica'] = Sala.objects.get(id=sala.id_sala).descricao_sala
                    subpedido['editar_sala_especifica'] = Sala.objects.get(id=sala.editar_id_sala).descricao_sala
                    subpedido['numero_alunos'] = 0
                elif(sala.acao == 3):
                    subpedido['sala_especifica'] = ""
                    subpedido['descricao'] = sala.descricao
                    subpedido['editar_descricao'] = sala.editar_descricao                
                    subpedido['inicio'] = sala.inicio
                    subpedido['editar_inicio'] = sala.editar_inicio
                    subpedido['fim'] = sala.fim
                    subpedido['editar_fim'] = sala.editar_fim
                    subpedido['instituicao'] = Instituicao.objects.get(id=sala.id_instituicao).nome_instituicao
                    subpedido['editar_instituicao'] = Instituicao.objects.get(id=sala.editar_id_instituicao).nome_instituicao
                    subpedido['edificio'] = Edificio.objects.get(id=sala.id_edificio).edificio
                    subpedido['editar_edificio'] = Edificio.objects.get(id=sala.editar_id_edificio).edificio
                    subpedido['tipo_sala'] = Categoria.objects.get(id=sala.categoria).tipo_de_sala
                    subpedido['editar_tipo_sala'] = Categoria.objects.get(id=sala.editar_categoria).tipo_de_sala
                    subpedido['tipodeaula'] = TipoDeAulas.objects.get(id=sala.id_tipo_de_aula).tipo_aula
                    subpedido['editar_tipodeaula'] = TipoDeAulas.objects.get(id=sala.editar_id_tipo_de_aula).tipo_aula   
                    subpedido['numero_alunos'] = sala.numero_alunos
                    subpedido['editar_numero_alunos'] = sala.editar_numero_alunos
                    subpedido['action'] = sala.acao 
                elif(sala.numero_alunos is None):
                    subpedido['descricao'] = sala.descricao              
                    subpedido['inicio'] = sala.inicio
                    subpedido['fim'] = sala.fim
                    subpedido['action'] = sala.acao
                    subpedido['sala_especifica'] = Sala.objects.get(id=sala.id_sala).descricao_sala
                    subpedido['numero_alunos'] = 0
                else:
                    subpedido['sala_especifica'] = ""
                    subpedido['descricao'] = sala.descricao           
                    subpedido['inicio'] = sala.inicio
                    subpedido['fim'] = sala.fim
                    subpedido['instituicao'] = Instituicao.objects.get(id=sala.id_instituicao).nome_instituicao
                    subpedido['edificio'] = Edificio.objects.get(id=sala.id_edificio).edificio
                    subpedido['tipo_sala'] = Categoria.objects.get(id=sala.categoria).tipo_de_sala
                    subpedido['tipodeaula'] = TipoDeAulas.objects.get(id=sala.id_tipo_de_aula).tipo_aula
                    subpedido['numero_alunos'] = sala.numero_alunos
                    subpedido['action'] = sala.acao 
                subpedidos.append(subpedido)
        elif pedido.tipo.id == 4:
            uc = SubpedidoUc.objects.filter(pedido_ptr_id=pedido.id)
            for ucs in uc:
                subpedido = {}
                subpedido['acao'] = ucs.acao
                subpedido['uc'] = Uc.objects.get(id=ucs.ucid).disciplina
                subpedido['turma'] = ucs.turma
                subpedido['descricao'] = ucs.descricao
                subpedidos.append(subpedido)
        pedido.subpedidos = subpedidos
    return render(request, 
                        template_name="pedido/obter_informacao_pcp.html",
                        context={'pedido':pedido,})