from django.http import HttpResponse


from .models import *
from main.models import *

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import *
from django.conf import settings
from django.contrib.auth.models import Group

from django.core.paginator import Paginator

from notifications.signals import notify
from django.utils import timezone

from datetime import datetime, timedelta

from .forms import *

from django.http import HttpResponseRedirect


def limpar_notificacoes(request, id):
    ''' Apagar notificacoes de um utilizadore por categorias '''
    if request.user.is_authenticated:
        user = get_user(request)
    else:
        return redirect('main:mensagem', 5)
    if id == 1:
        notificacoes = user.notifications.unread() 
    elif id ==2:
        notificacoes = user.notifications.read() 
    elif id == 3:
        notificacoes = Notificacao.objects.filter(recipient_id=user , public=False)
    elif id ==4:    
        notificacoes = Notificacao.objects.filter(recipient_id=user , public=True)
    elif id == 5:
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="info")
    elif id ==6:  
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="warning")
    elif id ==7: 
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="error")
    elif id ==8:  
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="success")
    else:
        notificacoes = user.notifications.all()
    for x in notificacoes:
        x.delete()

    return redirect('notificacoes:categorias-notificacao-automatica',0,0)




def marcar_como_lida(request):
    ''' Marcar todas as notificações de um utilizador como lidas '''
    if request.user.is_authenticated:
        user = get_user(request)
    else:
        return redirect('main:mensagem', 5)
    user.notifications.mark_all_as_read(user)
    return redirect('notificacoes:categorias-notificacao-automatica',0,0)






def sem_notificacoes(request, id):
    ''' Página quando não existem notificacoes '''
    if request.user.is_authenticated:
        user = get_user(request)
    else:
        return redirect('main:mensagem', 5)

    return render(request, 'notificacoes/sem_notificacoes.html', {
        'categoria':id,
    })

    

######################################################### Mensagens #####################################################


def escolher_tipo(request):
    ''' Escolher tipo de mensagem a enviar, poderá ser uma mensagem de grupo ou individual '''
    if request.user.is_authenticated:
        user = get_user(request)
    else:
        return redirect('main:mensagem', 5)
    groups = list(map(lambda a : a.name, user.groups.all()))
    if 'PCP' in groups: return render(request, 'notificacoes/escolher_tipo_mensagem.html',context={"user_type": 1})
    if 'Funcionario' in groups: return render(request, 'notificacoes/escolher_tipo_mensagem.html',context={"user_type": 0})
    if 'Docente' in groups: return redirect('notificacoes:escrever-mensagem', 0)


def concluir_envio(request):
    ''' Página de sucesso quando a mensagem é enviada '''
    if request.user.is_authenticated:
        user = get_user(request)
    else:
        return redirect('main:mensagem', 5)
    return render(request, 'notificacoes/concluir_envio.html')



def criar_mensagem(request, id):
    ''' Criar uma nova mensagem tomando em consideração o tipo de utilizador que está logado atualmente no sistema '''
    if request.user.is_authenticated: 
        user = get_user(request) 
        groups = list(map(lambda a : a.name, user.groups.all()))
        if 'Funcionario' in groups: user = Funcionario.objects.get(user_ptr_id=user.id)
        else: user = Docente.objects.get(user_ptr_id=user.id)
        return redirect('notificacoes:criar-mensagem-participante', id) 
    else:
        return redirect('main:mensagem', 5)      





def criar_mensagem_participante(request, id):
    ''' Criar uma nova mensagem por um participante '''
    msg = False
    if request.user.is_authenticated: 
        user = get_user(request) 
    else:
        return redirect('main:mensagem', 5)     
    groups = list(map(lambda a : a.name, user.groups.all()))
    docente = False
    if 'Docente' in groups: docente = True
    if id == 0: choices = map(lambda e : (e.id, e.get_full_name()) , Funcionario.objects.exclude(user_ptr_id=user))
    if id == 1: choices = map(lambda e : (e.id, e.get_full_name()) , Docente.objects.exclude(user_ptr_id=None))
    if request.method == "POST":
        tipo = id
        if tipo == 0 or tipo == 1:
            form = MensagemFormIndividualParticipante(choices, request.POST)
        elif tipo == 2 or tipo == 3:
            form = MensagemFormGrupoParticipante(request.POST)
        else:
            return redirect("main:mensagem",5)
        if form.is_valid():
            titulo = form.cleaned_data.get('titulo')
            mensagem = form.cleaned_data.get('mensagem')
            if tipo == 0 or tipo == 1:
                recipiente_id = form.cleaned_data.get('to')
                if tipo == 0: user_recipient = Funcionario.objects.get(user_ptr_id=recipiente_id)
                elif tipo == 1: user_recipient = Docente.objects.get(user_ptr_id=recipiente_id)
                info = InformacaoMensagem(data=timezone.now(), pendente=False, titulo = titulo,
                                descricao = mensagem, emissor = user , recetor = user_recipient, tipo = "Individual" , lido = False)
                info.save()
                mensagem1 = MensagemEnviada(mensagem=info)
                mensagem1.mensagem.lido = False
                mensagem1.save()
                mensagem2 = MensagemRecebida(mensagem=info)
                mensagem2.save()
                #sendNot(user.email, request.session['password'], user_recipient.email, "Mensagem Recebida do Sistema de Pedidos: " + titulo, mensagem)
            elif tipo == 2 or tipo == 3:
                if tipo == 2: utilizadores = Funcionario.objects.all()
                else: utilizadores = Docente.objects.exclude(user_ptr_id=None)
                for x in utilizadores:
                    user_recipient = x.user
                    info = InformacaoMensagem(data=timezone.now(), pendente=True, titulo = titulo,
                                    descricao = mensagem, emissor = user , recetor = user_recipient, tipo = "Grupo" , lido = False)
                    info.save()
                    if user_recipient.id != user.id:
                        tmp = MensagemRecebida(mensagem=info)
                        tmp.save() 
                    #sendNot(user.email, request.session['password'], user_recipient.email, "Mensagem de Grupo Recebida do Sistema de Pedidos: " + titulo, mensagem)
                mensagem1 = MensagemEnviada(mensagem=info)
                mensagem1.mensagem.lido = False
                mensagem1.save()    
            return redirect("notificacoes:concluir-envio")
        else:
            msg = True
            if tipo == 0 or tipo == 1:
                return render(request=request,
                    template_name="notificacoes/enviar_notificacao.html",
                    context={"form": form,"msg":msg, "docente": docente})
            elif tipo == 2 or tipo == 3:    
                form = MensagemFormGrupoParticipante()
                return render(request=request,
                    template_name="notificacoes/enviar_notificacao.html",
                    context={"form": form,"msg":msg, "docente": docente})
    else:
        tipo = id
        if tipo == 0 or tipo == 1:
            form = MensagemFormIndividualParticipante(choices)
            return render(request=request,
                  template_name="notificacoes/enviar_notificacao.html",
                  context={"form": form,"msg":msg, "docente": docente})
        elif tipo == 2 or tipo == 3:
            form = MensagemFormGrupoParticipante()
            return render(request=request,
                  template_name="notificacoes/enviar_notificacao.html",
                  context={"form": form,"msg":msg, "docente": docente})
        else:
            return redirect("main:mensagem",5)

def apagar_mensagem(request, id ,nr):
    ''' Apagar uma mensagem '''
    if request.user.is_authenticated:
        user = get_user(request)
    else:
        return redirect('main:mensagem', 5)
    m=""
    msg = False
    form = MensagemResposta()

    try:
        if id != 5:
            tmp = MensagemRecebida.objects.get(mensagem=nr)
        else:
            tmp = MensagemEnviada.objects.get(mensagem=nr)

        tmp.delete()
    except:
        return redirect('main:mensagem', 404)   
    
    page=request.GET.get('page')
    response = redirect('notificacoes:detalhes-mensagem', id, 0)
    response['Location'] += '?page='+page
    return response





def limpar_mensagens(request, id):
    ''' Apagar mensagens por categorias de um dado utilizador '''
    if request.user.is_authenticated:
        user = get_user(request)
    else:
        return redirect('main:mensagem', 5)

    if id == 5:
        notificacoes = MensagemEnviada.objects.select_related('mensagem__emissor').filter(mensagem__emissor=user.id)
    elif id == 1:
        notificacoes = MensagemRecebida.objects.select_related('mensagem__recetor').filter(mensagem__recetor=user.id,mensagem__lido=False) 
    elif id == 2:
        notificacoes = MensagemRecebida.objects.select_related('mensagem__recetor').filter(mensagem__recetor=user.id,mensagem__lido=True) 
    elif id == 3:
        notificacoes = MensagemRecebida.objects.select_related('mensagem__recetor').filter(mensagem__recetor=user.id,mensagem__pendente=False) 
    elif id == 4:    
        notificacoes = MensagemRecebida.objects.select_related('mensagem__recetor').filter(mensagem__recetor=user.id,mensagem__pendente=True)
    else:
        notificacoes = MensagemRecebida.objects.select_related('mensagem__recetor').filter(mensagem__recetor=user.id)
    
    for x in notificacoes:
        x.delete()

    return redirect('notificacoes:detalhes-mensagem',id,0)




def mensagem_como_lida(request, id):
    ''' Marcar todas as mensagens de um utilizador como lidas '''
    if request.user.is_authenticated:
        user = get_user(request)
    else:
        return redirect('main:mensagem', 5)
    msgs = MensagemRecebida.objects.select_related('mensagem__recetor').filter(mensagem__recetor=user.id)
    for msg in msgs:
        msg.mensagem.lido = True
        msg.mensagem.save()
        msg.save()
    return redirect('notificacoes:detalhes-mensagem',0,0)






def sem_mensagens(request, id):
    ''' Página quando não existem mensagens '''
    if request.user.is_authenticated:
        user = get_user(request)
    else:
        return redirect('main:mensagem', 5)

    return render(request, 'notificacoes/sem_mensagens.html', {
        'categoria':id,
    })




def detalhes_mensagens(request, id, nr):
    ''' Ver mensagens por categorias '''
    if request.user.is_authenticated:
        user = get_user(request)
    else:
        return redirect('main:mensagem', 5)
    m=""
    if request.method == "POST":
        msg = True
        form = MensagemResposta(request.POST)
        if form.is_valid():
            mensagem = form.cleaned_data.get('mensagem')
            msg_id = form.cleaned_data.get('msg_atual')
            user_sender = Funcionario.objects.get(user_ptr_id=user)
            notificacao = MensagemRecebida.objects.get(id=msg_id)
            if "Re: " in notificacao.mensagem.titulo:
                t = notificacao.mensagem.titulo
            else:
                t = "Re: "+notificacao.mensagem.titulo
            info = InformacaoMensagem(data=timezone.now(), pendente=False, titulo = t ,
                            descricao = mensagem, emissor = user_sender, recetor = notificacao.mensagem.emissor, tipo = "Individual" , lido = False)
            info.save()
            mensagem1 = MensagemEnviada(mensagem=info)
            mensagem1.mensagem.lido = False
            mensagem1.save()    
            mensagem2 = MensagemRecebida(mensagem=info)
            mensagem2.save()
            m = "Mensagem enviada com sucesso"
            form = MensagemResposta()
        else:
            m = ""  
    else:
        msg = False
        form = MensagemResposta()

    x = 0   
    if id == 1:
        notificacoes = MensagemRecebida.objects.select_related('mensagem__recetor').filter(mensagem__recetor=user.id,mensagem__lido=False).order_by('-id') 
    elif id == 2:
        notificacoes = MensagemRecebida.objects.select_related('mensagem__recetor').filter(mensagem__recetor=user.id,mensagem__lido=True).order_by('-id') 
    elif id == 3:
        notificacoes = MensagemRecebida.objects.select_related('mensagem__recetor').filter(mensagem__recetor=user.id,mensagem__pendente=False).order_by('-id') 
    elif id == 4:    
        notificacoes = MensagemRecebida.objects.select_related('mensagem__recetor').filter(mensagem__recetor=user.id,mensagem__pendente=True).order_by('-id')
    elif id == 5:    
        notificacoes = MensagemEnviada.objects.select_related('mensagem__emissor').filter(mensagem__emissor=user.id).order_by('-id')
    else:
        notificacoes = MensagemRecebida.objects.select_related('mensagem__recetor').filter(mensagem__recetor=user.id).order_by('-id')
    
    x = len(notificacoes)
    if nr!=0:
        try:
            if id != 5: notificacao = MensagemRecebida.objects.get(mensagem=nr)
            else: notificacao = MensagemEnviada.objects.get(mensagem=nr)
        except:
            if x>0:
                notificacao = notificacoes[0]
            else:
                return redirect("notificacoes:sem-mensagens", id)       
    else:
        if x>0:
            notificacao = notificacoes[0]
        else:
            return redirect("notificacoes:sem-mensagens", id) 

    nr_notificacoes_por_pagina = 5
    paginator= Paginator(notificacoes,nr_notificacoes_por_pagina)
    page=request.GET.get('page')
    notificacoes = paginator.get_page(page)
    total = x
    if notificacao != None:
        if id != 5:
            notificacao.mensagem.lido = True
            notificacao.mensagem.save()
            notificacao.save()
    else:
        return redirect("main:mensagem", 5)
    return render(request, 'notificacoes/detalhes_mensagens.html', {
        "form": form,'atual': notificacao, 'notificacoes':notificacoes,'categoria':id,'total':total,"msg": msg,"m":m
    })

