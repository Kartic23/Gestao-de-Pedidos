from django.shortcuts import render, redirect
from django.shortcuts import render
from django.views.generic.list import *
from django.shortcuts import redirect
from .forms import *
from django.contrib.auth import *
import datetime
from django.core.exceptions import ObjectDoesNotExist
from pedidos.models import *
import re



def consultar_ano_letivo(request):
    anos = ano_letivo.objects.all();
    for ano in anos:
        ano.dia_inicio = str(ano.dia_inicio)
        ano.dia_fim = str(ano.dia_fim)

    return render(request,
                  template_name="ano_letivo/consultar_ano_letivo.html",
                  context={'anos':anos})

def criar_ano_letivo(request):
    msg = False
    erros = ""
    if request.method == 'POST':
        form = AnoLetivoForm(request.POST)
        ano = request.POST.get('ano_letivo', '')
        dia_inicio =  request.POST.get('dia_inicio', '')
        dia_fim =  request.POST.get('dia_fim', '')
        ano_letivo_pattern = re.compile(r'^\d{4}/\d{2}$')
        if dia_inicio > dia_fim:
            msg = True
            erros = "A data inicio deve ser antes da data final"
            return render(request,
                  template_name="ano_letivo/criar_ano_letivo.html",
                  context={'form':form, 'msg':msg,'erros':erros})
        elif not ano_letivo_pattern.match(ano):
            msg = True
            erros = "O ano letivo deve estar no formato nnnn/nn"
            form = AnoLetivoForm()
            return render(request,
                  template_name="ano_letivo/criar_ano_letivo.html",
                  context={'form':form, 'msg':msg,'erros':erros})
        elif form.is_valid():
            try:
                ano_letivo.objects.get(ano_letivo=ano)
                erros = "Já existe um ano letivo para esse ano."
                msg = True
                return render(request, template_name="ano_letivo/criar_ano_letivo.html",
                    context={'erros': erros,'msg':msg,'form':form})
            except ObjectDoesNotExist:
                letivo = form.save(commit=False)
                letivo.ativo = "N"
                letivo.save()
                return redirect('main:mensagem',9)
        else:
            return render(request,
                  template_name="ano_letivo/criar_ano_letivo.html",
                  context={'form':form, 'msg':msg,'erros':erros})
    else:
        form = AnoLetivoForm()
        return render(request,
                  template_name="ano_letivo/criar_ano_letivo.html",
                  context={'form':form, 'msg':msg,'erros':erros})
    

def eliminar_ano_letivo(request,id):
    anoletivo = ano_letivo.objects.get(id=id)
    if request.method == 'POST':
        if 'confirmar' in request.POST:
            try:
                Pedido.objects.get(anoletivoid=id)
                return redirect('main:mensagem',16)
            except ObjectDoesNotExist:
                anoletivo.delete()
                return redirect('main:mensagem',10)
        else:
            return redirect('anoletivo:consultar-ano-letivo')
    else:
        return render(request, 'ano_letivo/eliminar_ano_letivo.html', {'ano_letivo_id': id})


def ativar_desativar_ano_letivo(request, id):
    if request.method == 'POST':
        if 'confirmar' in request.POST:
            hoje = datetime.date.today() 
            inicio = ano_letivo.objects.get(id=id).dia_inicio
            fim = ano_letivo.objects.get(id=id).dia_fim
            if hoje > inicio and hoje < fim:
                letivo = ano_letivo.objects.get(id=id)
                ano_letivo.objects.update(ativo="N")
                letivo.ativo = "S"
                letivo.save()
                return redirect('main:mensagem',11)
            else:
                return redirect('main:mensagem',13)
        else:
            return redirect('anoletivo:consultar-ano-letivo')
    else:
        return render(request, 'ano_letivo/ativar_desativar_ano_letivo.html', {'ano_letivo_id': id})
    

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
