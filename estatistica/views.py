from django.shortcuts import render
from pedidos.models import *
from django.contrib.auth import *
import datetime

def estatistica(request):
    return render(request,
                  template_name="estatistica.html")

def calcular_minutos_medios(user,estado):
    print( Pedido.objects.filter(estado_0=estado,funcionarioutilizadorid=user.id).all())
    pedidos = Pedido.objects.filter(estado_0=estado,funcionarioutilizadorid=user.id).all()
    if pedidos:
        tempo_medio = 0
        tempo_total = datetime.timedelta() 
        num_pedidos = 0
        
        for pedido in pedidos:
            tempo_total += pedido.data_de_validacao - pedido.data_de_associacao
            num_pedidos += 1
            
        if num_pedidos > 0:
            tempo_medio = tempo_total / num_pedidos

        if "day" in str(tempo_medio):
            dias = ""
            for i in range(0,len(str(tempo_medio))):
                if str(tempo_medio)[i] == ' ':
                    break;
                dias =  str(tempo_medio)[i]

            horario = str(tempo_medio).split(' ')[2].strip()
            horas = horario.split(':')[0].strip()
            minutos = horario.split(':')[1].strip()
            segundos = horario.split(':')[2].strip()
            segundos = segundos.split('.')[0].strip()
            minutos_total = round(int(dias) * (1440)  + int(horas) * 60 + int(minutos) + int(segundos)/60)
        else:
            horas = str(tempo_medio).split(':')[0].strip()
            minutos = str(tempo_medio).split(':')[1].strip()
            segundos = str(tempo_medio).split(':')[2].strip()
            segundos = segundos.split('.')[0].strip()
            minutos_total = round(int(horas) * 60 + int(minutos) + int(segundos)/60)
    else:
        minutos_total = 0

    return minutos_total


def calcular_minutos_medios_por_id(user,estado):
    pedidos = Pedido.objects.filter(estado_0=estado,funcionarioutilizadorid=user).all()
    if pedidos:
        tempo_medio = 0
        tempo_total = datetime.timedelta() 
        num_pedidos = 0
        
        for pedido in pedidos:
            tempo_total += pedido.data_de_validacao - pedido.data_de_associacao
            num_pedidos += 1
            
        if num_pedidos > 0:
            tempo_medio = tempo_total / num_pedidos

        if "day" in str(tempo_medio):
            dias = ""
            for i in range(0,len(str(tempo_medio))):
                if str(tempo_medio)[i] == ' ':
                    break;
                dias =  str(tempo_medio)[i]

            horario = str(tempo_medio).split(' ')[2].strip()
            horas = horario.split(':')[0].strip()
            minutos = horario.split(':')[1].strip()
            segundos = horario.split(':')[2].strip()
            segundos = segundos.split('.')[0].strip()
            minutos_total = round(int(dias) * (1440)  + int(horas) * 60 + int(minutos) + int(segundos)/60)
        else:
            horas = str(tempo_medio).split(':')[0].strip()
            minutos = str(tempo_medio).split(':')[1].strip()
            segundos = str(tempo_medio).split(':')[2].strip()
            segundos = segundos.split('.')[0].strip()
            minutos_total = round(int(horas) * 60 + int(minutos) + int(segundos)/60)
    else:
        minutos_total = 0

    return minutos_total

def calcular_minutos_medios_por_Tipo(user,estado,tipo):
    pedidos = Pedido.objects.filter(estado_0=estado,funcionarioutilizadorid=user.id,tipo=tipo).all()
    if pedidos:
        tempo_medio = 0
        tempo_total = datetime.timedelta() 
        num_pedidos = 0
        
        for pedido in pedidos:
            tempo_total += pedido.data_de_validacao - pedido.data_de_associacao
            num_pedidos += 1
            
        if num_pedidos > 0:
            tempo_medio = tempo_total / num_pedidos

        if "day" in str(tempo_medio):
            dias = ""
            for i in range(0,len(str(tempo_medio))):
                if str(tempo_medio)[i] == ' ':
                    break;
                dias =  str(tempo_medio)[i]

            horario = str(tempo_medio).split(' ')[2].strip()
            horas = horario.split(':')[0].strip()
            minutos = horario.split(':')[1].strip()
            segundos = horario.split(':')[2].strip()
            segundos = segundos.split('.')[0].strip()
            minutos_total = round(int(dias) * (1440)  + int(horas) * 60 + int(minutos) + int(segundos)/60)
        else:
            horas = str(tempo_medio).split(':')[0].strip()
            minutos = str(tempo_medio).split(':')[1].strip()
            segundos = str(tempo_medio).split(':')[2].strip()
            segundos = segundos.split('.')[0].strip()
            minutos_total = round(int(horas) * 60 + int(minutos) + int(segundos)/60)
    else:
        minutos_total = 0
    return minutos_total


def calcular_minutos_medios_por_intervalo_datas(user,estado,data_inicio,data_fim):
    pedidos = Pedido.objects.filter(estado_0=estado,funcionarioutilizadorid=user.id,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim)).all()
    if pedidos:
        tempo_medio = 0
        tempo_total = datetime.timedelta() 
        num_pedidos = 0
        
        for pedido in pedidos:
            tempo_total += pedido.data_de_validacao - pedido.data_de_associacao
            num_pedidos += 1
            
        if num_pedidos > 0:
            tempo_medio = tempo_total / num_pedidos

        if "day" in str(tempo_medio):
            dias = ""
            for i in range(0,len(str(tempo_medio))):
                if str(tempo_medio)[i] == ' ':
                    break;
                dias =  str(tempo_medio)[i]

            horario = str(tempo_medio).split(' ')[2].strip()
            horas = horario.split(':')[0].strip()
            minutos = horario.split(':')[1].strip()
            segundos = horario.split(':')[2].strip()
            segundos = segundos.split('.')[0].strip()
            minutos_total = round(int(dias) * (1440)  + int(horas) * 60 + int(minutos) + int(segundos)/60)
        else:
            horas = str(tempo_medio).split(':')[0].strip()
            minutos = str(tempo_medio).split(':')[1].strip()
            segundos = str(tempo_medio).split(':')[2].strip()
            segundos = segundos.split('.')[0].strip()
            minutos_total = round(int(horas) * 60 + int(minutos) + int(segundos)/60)
    else:
        minutos_total = 0
    return minutos_total





def calcular_minutos_medios_pcp(estado):
    pedidos = Pedido.objects.filter(estado_0=estado).all()
    if pedidos:
        tempo_medio = 0
        tempo_total = datetime.timedelta() 
        num_pedidos = 0
        
        for pedido in pedidos:
            tempo_total += pedido.data_de_validacao - pedido.data_de_associacao
            num_pedidos += 1
            
        if num_pedidos > 0:
            tempo_medio = tempo_total / num_pedidos

        if "day" in str(tempo_medio):
            dias = ""
            for i in range(0,len(str(tempo_medio))):
                if str(tempo_medio)[i] == ' ':
                    break;
                dias =  str(tempo_medio)[i]

            horario = str(tempo_medio).split(' ')[2].strip()
            horas = horario.split(':')[0].strip()
            minutos = horario.split(':')[1].strip()
            segundos = horario.split(':')[2].strip()
            segundos = segundos.split('.')[0].strip()
            minutos_total = round(int(dias) * (1440)  + int(horas) * 60 + int(minutos) + int(segundos)/60)
        else:
            horas = str(tempo_medio).split(':')[0].strip()
            minutos = str(tempo_medio).split(':')[1].strip()
            segundos = str(tempo_medio).split(':')[2].strip()
            segundos = segundos.split('.')[0].strip()
            minutos_total = round(int(horas) * 60 + int(minutos) + int(segundos)/60)
    else:
        minutos_total = 0
    return minutos_total


def calcular_minutos_medios_por_Tipo_pcp(estado,tipo):
    pedidos = Pedido.objects.filter(estado_0=estado,tipo=tipo).all()
    if pedidos:
        tempo_medio = 0
        tempo_total = datetime.timedelta() 
        num_pedidos = 0
        
        for pedido in pedidos:
            tempo_total += pedido.data_de_validacao - pedido.data_de_associacao
            num_pedidos += 1
            
        if num_pedidos > 0:
            tempo_medio = tempo_total / num_pedidos

        if "day" in str(tempo_medio):
            dias = ""
            for i in range(0,len(str(tempo_medio))):
                if str(tempo_medio)[i] == ' ':
                    break;
                dias =  str(tempo_medio)[i]

            horario = str(tempo_medio).split(' ')[2].strip()
            horas = horario.split(':')[0].strip()
            minutos = horario.split(':')[1].strip()
            segundos = horario.split(':')[2].strip()
            segundos = segundos.split('.')[0].strip()
            minutos_total = round(int(dias) * (1440)  + int(horas) * 60 + int(minutos) + int(segundos)/60)
        else:
            horas = str(tempo_medio).split(':')[0].strip()
            minutos = str(tempo_medio).split(':')[1].strip()
            segundos = str(tempo_medio).split(':')[2].strip()
            segundos = segundos.split('.')[0].strip()
            minutos_total = round(int(horas) * 60 + int(minutos) + int(segundos)/60)
    else:
        minutos_total = 0
    return minutos_total

def calcular_minutos_medios_por_intervalo_datas_pcp(estado,data_inicio,data_fim):
    pedidos = Pedido.objects.filter(estado_0=estado,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim)).all()
    if pedidos:
        tempo_medio = 0
        tempo_total = datetime.timedelta() 
        num_pedidos = 0
        
        for pedido in pedidos:
            tempo_total += pedido.data_de_validacao - pedido.data_de_associacao
            num_pedidos += 1
            
        if num_pedidos > 0:
            tempo_medio = tempo_total / num_pedidos

        if "day" in str(tempo_medio):
            dias = ""
            for i in range(0,len(str(tempo_medio))):
                if str(tempo_medio)[i] == ' ':
                    break;
                dias =  str(tempo_medio)[i]

            horario = str(tempo_medio).split(' ')[2].strip()
            horas = horario.split(':')[0].strip()
            minutos = horario.split(':')[1].strip()
            segundos = horario.split(':')[2].strip()
            segundos = segundos.split('.')[0].strip()
            minutos_total = round(int(dias) * (1440)  + int(horas) * 60 + int(minutos) + int(segundos)/60)
        else:
            horas = str(tempo_medio).split(':')[0].strip()
            minutos = str(tempo_medio).split(':')[1].strip()
            segundos = str(tempo_medio).split(':')[2].strip()
            segundos = segundos.split('.')[0].strip()
            minutos_total = round(int(horas) * 60 + int(minutos) + int(segundos)/60)
    else:
        minutos_total = 0
    return minutos_total


def minutos_para_tempo(minutos):
    dias = int ((minutos/60) / (24))
    horas = int(minutos / 60) 
    minuto = minutos
    segundos = minutos * 60
    
    valores =[]
    valores.append(dias)
    valores.append(horas)
    valores.append(minuto)
    valores.append(segundos)
    
    return valores


def tempo_medio_funcionario(request):
    user = get_user(request)
    if request.method == 'POST':
        opcao = request.POST.get('selected_option')
        minutos_total_aceites = 0
        minutos_total_rejeitados = 0
        tipohorario = request.POST.get('horario')
        tipooutros = request.POST.get('outros')
        tiposala = request.POST.get('sala')
        tipouc = request.POST.get('uc')
        if tipohorario == 'horario':
            minutos_total_aceites += calcular_minutos_medios_por_Tipo(user,3,1)
            minutos_total_rejeitados += calcular_minutos_medios_por_Tipo(user,4,1)
        if tipooutros == 'outros':
            minutos_total_aceites += calcular_minutos_medios_por_Tipo(user,3,2)
            minutos_total_rejeitados += calcular_minutos_medios_por_Tipo(user,4,2)
        if tiposala == 'sala':
            minutos_total_aceites += calcular_minutos_medios_por_Tipo(user,3,3)
            minutos_total_rejeitados += calcular_minutos_medios_por_Tipo(user,4,3)
        if tipouc == 'uc':
            minutos_total_aceites += calcular_minutos_medios_por_Tipo(user,3,4)
            minutos_total_rejeitados += calcular_minutos_medios_por_Tipo(user,4,4)
    
        data_inicio = request.POST.get('data_de_inicio')
        data_fim = request.POST.get('data_de_fim')
        if data_inicio != "":
            minutos_total_aceites += calcular_minutos_medios_por_intervalo_datas(user,3,data_inicio,data_fim)
            minutos_total_rejeitados += calcular_minutos_medios_por_intervalo_datas(user,4,data_inicio,data_fim)
        
        if data_inicio == "" and tipohorario == None and tipooutros == None and tiposala == None and tipouc == None:
            minutos_total_aceites += calcular_minutos_medios(user,3)
            minutos_total_rejeitados += calcular_minutos_medios(user,4)

        valores_aceites = minutos_para_tempo(minutos_total_aceites)
        valores_rejeitados = minutos_para_tempo(minutos_total_rejeitados)
        return render(request,
                  template_name="tempo_medio_funcionario.html",
                  context={'tempo_medio_aceites':minutos_total_aceites,'tempo_medio_rejeitados':minutos_total_rejeitados,
                           'valores_a': valores_aceites,'valores_r':valores_rejeitados})
    else:
        minutos_total_aceites = calcular_minutos_medios(user,3)
        minutos_total_rejeitados = calcular_minutos_medios(user,4)
        valores_aceites = minutos_para_tempo(minutos_total_aceites)
        valores_rejeitados = minutos_para_tempo(minutos_total_rejeitados)
        return render(request,
                  template_name="tempo_medio_funcionario.html",
                  context={'tempo_medio_aceites':minutos_total_aceites,'tempo_medio_rejeitados':minutos_total_rejeitados,
                           'valores_a': valores_aceites,'valores_r':valores_rejeitados})
    


def tempo_medio_pcp(request):
    lista_de_funcionarios = Funcionario.objects.all()
    if request.method == 'POST':
        opcao = request.POST.get('selected_option')
        minutos_total_aceites = 0
        minutos_total_rejeitados = 0
        tipohorario = request.POST.get('horario')
        tipooutros = request.POST.get('outros')
        tiposala = request.POST.get('sala')
        tipouc = request.POST.get('uc')

        if tipohorario == 'horario':
            minutos_total_aceites += calcular_minutos_medios_por_Tipo_pcp(3,1)
            minutos_total_rejeitados += calcular_minutos_medios_por_Tipo_pcp(4,1)
        if tipooutros == 'outros':
            minutos_total_aceites += calcular_minutos_medios_por_Tipo_pcp(3,2)
            minutos_total_rejeitados += calcular_minutos_medios_por_Tipo_pcp(4,2)
        if tiposala == 'sala':
            minutos_total_aceites += calcular_minutos_medios_por_Tipo_pcp(3,3)
            minutos_total_rejeitados += calcular_minutos_medios_por_Tipo_pcp(4,3)
        if tipouc == 'uc':
            minutos_total_aceites += calcular_minutos_medios_por_Tipo_pcp(3,4)
            minutos_total_rejeitados += calcular_minutos_medios_por_Tipo_pcp(4,4)
        
        
        data_inicio = request.POST.get('data_de_inicio')
        data_fim = request.POST.get('data_de_fim')
        if data_inicio != "":
            minutos_total_aceites += calcular_minutos_medios_por_intervalo_datas_pcp(3,data_inicio,data_fim)
            minutos_total_rejeitados = calcular_minutos_medios_por_intervalo_datas_pcp(4,data_inicio,data_fim)
        funcionario_id = request.POST.get('funcionarios')        
        if funcionario_id != "":
            minutos_total_aceites += calcular_minutos_medios_por_id(funcionario_id,3)
            minutos_total_rejeitados = calcular_minutos_medios_por_id(funcionario_id,4)

        if data_inicio == "" and tipohorario == None and tipooutros == None and tiposala == None and tipouc == None and funcionario_id == "":
            print(funcionario_id)    
            minutos_total_aceites = calcular_minutos_medios_pcp(3)
            minutos_total_rejeitados = calcular_minutos_medios_pcp(4)
        valores_aceites = minutos_para_tempo(minutos_total_aceites)
        valores_rejeitados = minutos_para_tempo(minutos_total_rejeitados)
        return render(request,
                  template_name="tempo_medio_pcp.html",
                  context={'tempo_medio_aceites':minutos_total_aceites,'tempo_medio_rejeitados':minutos_total_rejeitados,
                           'funcionarios': lista_de_funcionarios,'valores_a': valores_aceites,'valores_r':valores_rejeitados})
    else:
        minutos_total_aceites = calcular_minutos_medios_pcp(3)
        minutos_total_rejeitados = calcular_minutos_medios_pcp(4)
        valores_aceites = minutos_para_tempo(minutos_total_aceites)
        valores_rejeitados = minutos_para_tempo(minutos_total_rejeitados)
        return render(request,
                  template_name="tempo_medio_pcp.html",
                  context={'tempo_medio_aceites':minutos_total_aceites,'tempo_medio_rejeitados':minutos_total_rejeitados,
                           'funcionarios': lista_de_funcionarios,'valores_a': valores_aceites,'valores_r':valores_rejeitados})
    



def estatistica_pedido_funcionario(request):
    user = get_user(request)
    funcionarios = Docente.objects.filter(is_active=1).all()

    if request.method == 'POST':
        pedidos_em_espera=0
        pedidos_analise=0
        pedidos_concluido=0
        pedidos_rejeitados = 0
        

        tipohorario = request.POST.get('horario')
        tipooutros = request.POST.get('outros')
        tiposala = request.POST.get('sala')
        tipouc = request.POST.get('uc')
        data_inicio = request.POST.get('data_de_inicio')
        data_fim = request.POST.get('data_de_fim')



        if tipohorario == 'horario' and data_fim != "" and data_inicio != "":
                
                pedidos_em_espera += Pedido.objects.filter(estado_0=1,tipo=1,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim)).count() #pendente
                pedidos_analise += Pedido.objects.filter(estado_0=2,tipo=1,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim)).count() #analise
                pedidos_concluido += Pedido.objects.filter(estado_0=3,tipo=1,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim)).count() #aceite
                pedidos_rejeitados += Pedido.objects.filter(estado_0=4,tipo=1,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim)).count() #rejeitado
        
        elif tipohorario == 'horario':
                
                pedidos_em_espera += Pedido.objects.filter(estado_0=1,tipo=1).count() #pendente
                pedidos_analise += Pedido.objects.filter(estado_0=2,tipo=1).count() #analise
                pedidos_concluido += Pedido.objects.filter(estado_0=3,tipo=1).count() #aceite
                pedidos_rejeitados += Pedido.objects.filter(estado_0=4,tipo=1).count() #rejeitado


        if tipooutros == 'outros' and data_fim != "" and data_inicio != "":
                
                pedidos_em_espera += Pedido.objects.filter(estado_0=1,tipo=2,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim)).count() #pendente
                pedidos_analise += Pedido.objects.filter(estado_0=2,tipo=2,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim)).count() #analise
                pedidos_concluido += Pedido.objects.filter(estado_0=3,tipo=2,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim)).count() #aceite
                pedidos_rejeitados += Pedido.objects.filter(estado_0=4,tipo=2,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim)).count() #rejeitado
        
        elif tipooutros == 'outros':
                
                pedidos_em_espera += Pedido.objects.filter(estado_0=1,tipo=2).count() #pendente
                pedidos_analise += Pedido.objects.filter(estado_0=2,tipo=2).count() #analise
                pedidos_concluido += Pedido.objects.filter(estado_0=3,tipo=2).count() #aceite
                pedidos_rejeitados += Pedido.objects.filter(estado_0=4,tipo=2).count() #rejeitado


        if tiposala == 'sala' and data_fim != "" and data_inicio != "":
                
                pedidos_em_espera += Pedido.objects.filter(estado_0=1,tipo=3,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim)).count() #pendente
                pedidos_analise += Pedido.objects.filter(estado_0=2,tipo=3,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim)).count() #analise
                pedidos_concluido += Pedido.objects.filter(estado_0=3,tipo=3,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim)).count() #aceite
                pedidos_rejeitados += Pedido.objects.filter(estado_0=4,tipo=3,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim)).count() #rejeitado
        
        elif tiposala == 'sala':
                
                pedidos_em_espera += Pedido.objects.filter(estado_0=1,tipo=3).count() #pendente
                pedidos_analise += Pedido.objects.filter(estado_0=2,tipo=3).count() #analise
                pedidos_concluido += Pedido.objects.filter(estado_0=3,tipo=3).count() #aceite
                pedidos_rejeitados += Pedido.objects.filter(estado_0=4,tipo=3).count() #rejeitado

        if tipouc == 'uc' and data_fim != "" and data_inicio != "":
                
                pedidos_em_espera += Pedido.objects.filter(estado_0=1,tipo=4,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim)).count() #pendente
                pedidos_analise += Pedido.objects.filter(estado_0=2,tipo=4,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim)).count() #analise
                pedidos_concluido += Pedido.objects.filter(estado_0=3,tipo=4,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim)).count() #aceite
                pedidos_rejeitados += Pedido.objects.filter(estado_0=4,tipo=4,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim)).count() #rejeitado
        
        elif tipouc == 'uc':
                
                pedidos_em_espera += Pedido.objects.filter(estado_0=1,tipo=4).count() #pendente
                pedidos_analise += Pedido.objects.filter(estado_0=2,tipo=4).count() #analise
                pedidos_concluido += Pedido.objects.filter(estado_0=3,tipo=4).count() #aceite
                pedidos_rejeitados += Pedido.objects.filter(estado_0=4,tipo=4).count() #rejeitado


        if tipohorario == '' and tipooutros == '' and tiposala == '' and tipouc == '' and data_fim != "" and data_inicio != "":
                
            pedidos_em_espera = Pedido.objects.filter(estado_0=1,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim)).count() #pendente
            pedidos_analise = Pedido.objects.filter(estado_0=2,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim)).count() #analise
            pedidos_concluido = Pedido.objects.filter(estado_0=3,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim)).count() #aceite
            pedidos_rejeitados += Pedido.objects.filter(estado_0=4,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim)).count() #rejeitado
            
        funcionario_id = request.POST.get('funcionarios')

        if funcionario_id != "":
            funcionario_id = request.POST.get('funcionarios')  
            print(funcionario_id)
            pedidos_em_espera = Pedido.objects.filter(estado_0=1,docenteutilizadorid=funcionario_id).count() #rejeitado
            pedidos_analise = Pedido.objects.filter(estado_0=2,docenteutilizadorid=funcionario_id).count() #rejeitado
            pedidos_concluido +=  Pedido.objects.filter(estado_0=3,docenteutilizadorid=funcionario_id).count() #rejeitado
            pedidos_rejeitados += Pedido.objects.filter(estado_0=4,docenteutilizadorid=funcionario_id).count() #rejeitado

        if tipohorario == None and tipooutros == None and tiposala == None and tipouc == None and data_fim == "" and data_inicio == "" and funcionario_id == "":
            pedidos_em_espera += Pedido.objects.filter(estado_0=1).count() #pendente
            pedidos_analise += Pedido.objects.filter(estado_0=2).count() #analise
            pedidos_concluido += Pedido.objects.filter(estado_0=3).count() #aceite
            pedidos_rejeitados += Pedido.objects.filter(estado_0=4).count() #rejeitado

            

        return render(request,
                  template_name="estatistica_pedido_funcionario.html",
                  context={'pedidos_em_espera':pedidos_em_espera,'pedidos_analise':pedidos_analise,'pedidos_aceites':pedidos_concluido,'pedidos_rejeitados':pedidos_rejeitados, 'funcionarios':funcionarios})
    else:
        return render(request,
                  template_name="estatistica_pedido_funcionario.html",
                  context={'pedidos_em_espera':0,'pedidos_analise':0,'pedidos_concluido':0, 'funcionarios':funcionarios})


def estatistica_pedido_docente(request):
    user = get_user(request)
    if request.method == 'POST':
        
        pedidos_em_espera=0
        pedidos_analise=0
        pedidos_concluido=0
        pedidos_rejeitados=0
        
        tipohorario = request.POST.get('horario')
        tipooutros = request.POST.get('outros')
        tiposala = request.POST.get('sala')
        tipouc = request.POST.get('uc')
        data_inicio = request.POST.get('data_de_inicio')
        data_fim = request.POST.get('data_de_fim')



        if tipohorario == 'horario' and data_fim != "" and data_inicio != "":
                
                pedidos_em_espera += Pedido.objects.filter(estado_0=1,tipo=1,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim),docenteutilizadorid=user.id).count() #pendente
                pedidos_analise += Pedido.objects.filter(estado_0=2,tipo=1,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim),docenteutilizadorid=user.id).count() #analise
                pedidos_concluido += Pedido.objects.filter(estado_0=3,tipo=1,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim),docenteutilizadorid=user.id).count() #aceite
                pedidos_rejeitados += Pedido.objects.filter(estado_0=4,tipo=1,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim),docenteutilizadorid=user.id).count() #rejeitado
        
        elif tipohorario == 'horario':
                
                pedidos_em_espera += Pedido.objects.filter(estado_0=1,tipo=1,docenteutilizadorid=user.id).count() #pendente
                pedidos_analise += Pedido.objects.filter(estado_0=2,tipo=1,docenteutilizadorid=user.id).count() #analise
                pedidos_concluido += Pedido.objects.filter(estado_0=3,tipo=1,docenteutilizadorid=user.id).count() #aceite
                pedidos_rejeitados += Pedido.objects.filter(estado_0=4,tipo=1,docenteutilizadorid=user.id).count() #rejeitado


        if tipooutros == 'outros' and data_fim != "" and data_inicio != "":
                
                pedidos_em_espera += Pedido.objects.filter(estado_0=1,tipo=2,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim),docenteutilizadorid=user.id).count() #pendente
                pedidos_analise += Pedido.objects.filter(estado_0=2,tipo=2,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim),docenteutilizadorid=user.id).count() #analise
                pedidos_concluido += Pedido.objects.filter(estado_0=3,tipo=2,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim),docenteutilizadorid=user.id).count() #aceite
                pedidos_rejeitados += Pedido.objects.filter(estado_0=4,tipo=2,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim),docenteutilizadorid=user.id).count() #rejeitado
        
        elif tipooutros == 'outros':
                
                pedidos_em_espera += Pedido.objects.filter(estado_0=1,tipo=2,docenteutilizadorid=user.id).count() #pendente
                pedidos_analise += Pedido.objects.filter(estado_0=2,tipo=2,docenteutilizadorid=user.id).count() #analise
                pedidos_concluido += Pedido.objects.filter(estado_0=3,tipo=2,docenteutilizadorid=user.id).count() #aceite
                pedidos_rejeitados += Pedido.objects.filter(estado_0=4,tipo=2,docenteutilizadorid=user.id).count() #rejeitado


        if tiposala == 'sala' and data_fim != "" and data_inicio != "":
                
                pedidos_em_espera += Pedido.objects.filter(estado_0=1,tipo=3,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim),docenteutilizadorid=user.id).count() #pendente
                pedidos_analise += Pedido.objects.filter(estado_0=2,tipo=3,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim),docenteutilizadorid=user.id).count() #analise
                pedidos_concluido += Pedido.objects.filter(estado_0=3,tipo=3,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim),docenteutilizadorid=user.id).count() #aceite
                pedidos_rejeitados += Pedido.objects.filter(estado_0=4,tipo=3,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim),docenteutilizadorid=user.id).count() #rejeitado
        
        elif tiposala == 'sala':
                
                pedidos_em_espera += Pedido.objects.filter(estado_0=1,tipo=3,docenteutilizadorid=user.id).count() #pendente
                pedidos_analise += Pedido.objects.filter(estado_0=2,tipo=3,docenteutilizadorid=user.id).count() #analise
                pedidos_concluido += Pedido.objects.filter(estado_0=3,tipo=3,docenteutilizadorid=user.id).count() #aceite
                pedidos_rejeitados += Pedido.objects.filter(estado_0=4,tipo=3,docenteutilizadorid=user.id).count() #rejeitado

        if tipouc == 'uc' and data_fim != "" and data_inicio != "":
                
                pedidos_em_espera += Pedido.objects.filter(estado_0=1,tipo=4,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim),docenteutilizadorid=user.id).count() #pendente
                pedidos_analise += Pedido.objects.filter(estado_0=2,tipo=4,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim),docenteutilizadorid=user.id).count() #analise
                pedidos_concluido += Pedido.objects.filter(estado_0=3,tipo=4,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim),docenteutilizadorid=user.id).count() #aceite
                pedidos_rejeitados += Pedido.objects.filter(estado_0=4,tipo=4,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim),docenteutilizadorid=user.id).count() #rejeitado
        
        elif tipouc == 'uc':
                
                pedidos_em_espera += Pedido.objects.filter(estado_0=1,tipo=4,docenteutilizadorid=user.id).count() #pendente
                pedidos_analise += Pedido.objects.filter(estado_0=2,tipo=4,docenteutilizadorid=user.id).count() #analise
                pedidos_concluido += Pedido.objects.filter(estado_0=3,tipo=4,docenteutilizadorid=user.id).count() #aceite
                pedidos_rejeitados += Pedido.objects.filter(estado_0=4,tipo=4,docenteutilizadorid=user.id).count() #rejeitado


        if tipohorario == '' and tipooutros == '' and tiposala == '' and tipouc == '' and data_fim != "" and data_inicio != "":
                
            pedidos_em_espera = Pedido.objects.filter(estado_0=1,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim),docenteutilizadorid=user.id).count() #pendente
            pedidos_analise = Pedido.objects.filter(estado_0=2,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim),docenteutilizadorid=user.id).count() #analise
            pedidos_concluido = Pedido.objects.filter(estado_0=3,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim),docenteutilizadorid=user.id).count() #aceite
            pedidos_rejeitados += Pedido.objects.filter(estado_0=4,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim),docenteutilizadorid=user.id).count() #rejeitado


        if tipohorario == None and tipooutros == None and tiposala == None and tipouc == None and data_fim == "" and data_inicio == "" :
            pedidos_em_espera += Pedido.objects.filter(estado_0=1,docenteutilizadorid=user.id).count() #pendente
            pedidos_analise += Pedido.objects.filter(estado_0=2,docenteutilizadorid=user.id).count() #analise
            pedidos_concluido += Pedido.objects.filter(estado_0=3,docenteutilizadorid=user.id).count() #aceite
            pedidos_rejeitados += Pedido.objects.filter(estado_0=4,docenteutilizadorid=user.id).count() #rejeitado

               
        return render(request,
                  template_name="estatistica_pedido_docente.html",
                  context={'pedidos_em_espera':pedidos_em_espera,'pedidos_analise':pedidos_analise,'pedidos_aceites':pedidos_concluido, 'pedidos_rejeitados':pedidos_rejeitados})
    else:
        return render(request,
                  template_name="estatistica_pedido_docente.html",
                  context={'pedidos_em_espera':0,'pedidos_analise':0,'pedidos_aceites':0, 'pedidos_rejeitados':0})





######################################################################################################################################################
########################################################### ESTATISTICA PEDIDOS DAN ##################################################################
######################################################################################################################################################


def calcular_pedidos_medios(user,estado):
    pedidos = Pedido.objects.filter(estado_0=estado,funcionarioutilizadorid=user.id).all()
    if pedidos:
        pedidos_ace = 0
        pedidos_rej = 0
        num_pedidos = 0
        
        for pedido in pedidos:
            if (pedido.estado_0 == 3):
                pedidos_ace += 1
            elif (pedido.estado_0 == 4):
                pedidos_rej += 1
            num_pedidos += 1
    else:
        num_pedidos = 0
    return num_pedidos


def calcular_pedidos_medios_por_id(user,estado):
    pedidos = Pedido.objects.filter(estado_0=estado,funcionarioutilizadorid=user).all()
    if pedidos:
        pedidos_ace = 0
        pedidos_rej = 0
        num_pedidos = 0
        
        for pedido in pedidos:
            if (pedido.estado_0 == 3):
                pedidos_ace += 1
            elif (pedido.estado_0 == 4):
                pedidos_rej += 1
            num_pedidos += 1
    else:
        num_pedidos = 0
    return num_pedidos

def calcular_pedidos_medios_por_Tipo(user,estado,tipo):
    pedidos = Pedido.objects.filter(estado_0=estado,funcionarioutilizadorid=user.id,tipo=tipo).all()
    if pedidos:
        pedidos_ace = 0
        pedidos_rej = 0
        num_pedidos = 0
        
        for pedido in pedidos:
            if (pedido.estado_0 == 3):
                pedidos_ace += 1
            elif (pedido.estado_0 == 4):
                pedidos_rej += 1
            num_pedidos += 1
    else:
        num_pedidos = 0
    return num_pedidos



def calcular_pedidos_medios_por_intervalo_datas(user,estado,data_inicio,data_fim):
    pedidos = Pedido.objects.filter(estado_0=estado,funcionarioutilizadorid=user.id,data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim)).all()
    if pedidos:
        pedidos_ace = 0
        pedidos_rej = 0
        num_pedidos = 0
        
        for pedido in pedidos:
            if (pedido.estado_0 == 3):
                pedidos_ace += 1
            elif (pedido.estado_0 == 4):
                pedidos_rej += 1
            num_pedidos += 1
    else:
        num_pedidos = 0
    return num_pedidos

def calcular_pedidos_medios_pcp(estado):
    pedidos = Pedido.objects.filter(estado_0=estado).all()
    if pedidos:
        pedidos_ace = 0
        pedidos_rej = 0
        num_pedidos = 0
        
        for pedido in pedidos:
            if (pedido.estado_0 == 3):
                pedidos_ace += 1
            elif (pedido.estado_0 == 4):
                pedidos_rej += 1
            num_pedidos += 1
    else:
        num_pedidos = 0
    return num_pedidos


def calcular_pedidos_medios_por_id_pcp(user,estado):
    pedidos = Pedido.objects.filter(estado_0=estado,funcionarioutilizadorid=user).all()
    if pedidos:
        pedidos_ace = 0
        pedidos_rej = 0
        num_pedidos = 0
        
        for pedido in pedidos:
            if (pedido.estado_0 == 3):
                pedidos_ace += 1
            elif (pedido.estado_0 == 4):
                pedidos_rej += 1
            num_pedidos += 1
    else:
        num_pedidos = 0
    return num_pedidos

def calcular_pedidos_medios_por_Tipo_pcp(estado, tipo):
    pedidos = Pedido.objects.filter(estado_0=estado, tipo=tipo).all()
    if pedidos:
        pedidos_ace = 0
        pedidos_rej = 0
        num_pedidos = 0
        
        for pedido in pedidos:
            if (pedido.estado_0 == 3):
                pedidos_ace += 1
            elif (pedido.estado_0 == 4):
                pedidos_rej += 1
            num_pedidos += 1
    else:
        num_pedidos = 0
    return num_pedidos



def calcular_pedidos_medios_por_intervalo_datas_pcp(estado,data_inicio,data_fim):
    pedidos = Pedido.objects.filter(estado_0=estado, data_de_associacao__range=(data_inicio, data_fim),data_de_validacao__range=(data_inicio, data_fim)).all()
    if pedidos:
        pedidos_ace = 0
        pedidos_rej = 0
        num_pedidos = 0
        
        for pedido in pedidos:
            if (pedido.estado_0 == 3):
                pedidos_ace += 1
            elif (pedido.estado_0 == 4):
                pedidos_rej += 1
            num_pedidos += 1
    else:
        num_pedidos = 0
    return num_pedidos


def media_para_pedidos(pedidos, pedidos_totais):
    if (pedidos_totais == 0):
        valores = []
        valores.append('0')
        valores.append('None')
    else:
        n_pedidos = pedidos
        percentagem = str((pedidos / pedidos_totais) * 100) + '%'

        valores = []
        valores.append(n_pedidos)
        valores.append(percentagem)

    return valores


def pedidos_medio_funcionario(request):
    user = get_user(request)
    if request.method == 'POST':
        opcao = request.POST.get('selected_option')
        pedidos_total_aceites = 0
        pedidos_total_rejeitados = 0
        tipohorario = request.POST.get('horario')
        tipooutros = request.POST.get('outros')
        tiposala = request.POST.get('sala')
        tipouc = request.POST.get('uc')
        if tipohorario == 'horario':
            pedidos_total_aceites += calcular_pedidos_medios_por_Tipo(user,3,1)
            pedidos_total_rejeitados += calcular_pedidos_medios_por_Tipo(user,4,1)
        if tipooutros == 'outros':
            pedidos_total_aceites += calcular_pedidos_medios_por_Tipo(user,3,2)
            pedidos_total_rejeitados += calcular_pedidos_medios_por_Tipo(user,4,2)
        if tiposala == 'sala':
            pedidos_total_aceites += calcular_pedidos_medios_por_Tipo(user,3,3)
            pedidos_total_rejeitados += calcular_pedidos_medios_por_Tipo(user,4,3)
        if tipouc == 'uc':
            pedidos_total_aceites += calcular_pedidos_medios_por_Tipo(user,3,4)
            pedidos_total_rejeitados += calcular_pedidos_medios_por_Tipo(user,4,4)

        data_inicio = request.POST.get('data_de_inicio')
        data_fim = request.POST.get('data_de_fim')
        if data_inicio != "":
            pedidos_total_aceites += calcular_pedidos_medios_por_intervalo_datas(user,3,data_inicio,data_fim)
            pedidos_total_rejeitados += calcular_pedidos_medios_por_intervalo_datas(user,4,data_inicio,data_fim)
        
        if data_inicio == "" and tipohorario == None and tipooutros == None and tiposala == None and tipouc == None:
            pedidos_total_aceites = calcular_pedidos_medios(user,3)
            pedidos_total_rejeitados = calcular_pedidos_medios(user,4)

        valores_aceites = media_para_pedidos(pedidos_total_aceites, pedidos_total_aceites + pedidos_total_rejeitados)
        valores_rejeitados = media_para_pedidos(pedidos_total_rejeitados, pedidos_total_aceites + pedidos_total_rejeitados)

        return render(request,
                  template_name="pedidos_medio_funcionario.html",
                  context={'pedidos_medio_aceites':pedidos_total_aceites,'pedidos_medio_rejeitados':pedidos_total_rejeitados,
                           'valores_a': valores_aceites, 'valores_r': valores_rejeitados})
    else:
        pedidos_total_aceites = calcular_pedidos_medios(user,3)
        pedidos_total_rejeitados = calcular_pedidos_medios(user,4)
        valores_aceites = media_para_pedidos(pedidos_total_aceites, pedidos_total_aceites + pedidos_total_rejeitados)
        valores_rejeitados = media_para_pedidos(pedidos_total_rejeitados, pedidos_total_aceites + pedidos_total_rejeitados)
        return render(request,
                  template_name="pedidos_medio_funcionario.html",
                  context={'pedidos_medio_aceites':pedidos_total_aceites,'pedidos_medio_rejeitados':pedidos_total_rejeitados,
                           'valores_a': valores_aceites, 'valores_r': valores_rejeitados})


def pedidos_medio_pcp(request):
    lista_de_funcionarios = Funcionario.objects.all()
    if request.method == 'POST':
        opcao = request.POST.get('selected_option')
        pedidos_total_aceites = 0
        pedidos_total_rejeitados = 0
        tipohorario = request.POST.get('horario')
        tipooutros = request.POST.get('outros')
        tiposala = request.POST.get('sala')
        tipouc = request.POST.get('uc')
        
        if tipohorario == 'horario':
            pedidos_total_aceites += calcular_pedidos_medios_por_Tipo_pcp(3,1)
            pedidos_total_rejeitados += calcular_pedidos_medios_por_Tipo_pcp(4,1)
        if tipooutros == 'outros':
            pedidos_total_aceites += calcular_pedidos_medios_por_Tipo_pcp(3,2)
            pedidos_total_rejeitados += calcular_pedidos_medios_por_Tipo_pcp(4,2)
        if tiposala == 'sala':
            pedidos_total_aceites += calcular_pedidos_medios_por_Tipo_pcp(3,3)
            pedidos_total_rejeitados += calcular_pedidos_medios_por_Tipo_pcp(4,3)
        if tipouc == 'uc':
            pedidos_total_aceites += calcular_pedidos_medios_por_Tipo_pcp(3,4)
            pedidos_total_rejeitados += calcular_pedidos_medios_por_Tipo_pcp(4,4)

        data_inicio = request.POST.get('data_de_inicio')
        data_fim = request.POST.get('data_de_fim')
        if data_inicio != "":
            pedidos_total_aceites += calcular_pedidos_medios_por_intervalo_datas_pcp(3,data_inicio,data_fim)
            pedidos_total_rejeitados = calcular_pedidos_medios_por_intervalo_datas_pcp(4,data_inicio,data_fim)
        funcionario_id = request.POST.get('funcionarios')
        if funcionario_id != "":
            funcionario_id = request.POST.get('funcionarios')        
            print(funcionario_id)    
            pedidos_total_aceites += calcular_pedidos_medios_por_id_pcp(funcionario_id,3)
            pedidos_total_rejeitados = calcular_pedidos_medios_por_id_pcp(funcionario_id,4)
        
        valores_aceites = media_para_pedidos(pedidos_total_aceites, pedidos_total_aceites + pedidos_total_rejeitados)
        valores_rejeitados = media_para_pedidos(pedidos_total_rejeitados, pedidos_total_aceites + pedidos_total_rejeitados)

        return render(request,
                  template_name="pedidos_medio_pcp.html",
                  context={'pedidos_medio_aceites':pedidos_total_aceites,'pedidos_medio_rejeitados':pedidos_total_rejeitados,
                           'funcionarios': lista_de_funcionarios, 'valores_a': valores_aceites, 'valores_r': valores_rejeitados})
    else:
        pedidos_total_aceites = calcular_pedidos_medios_pcp(3)
        pedidos_total_rejeitados = calcular_pedidos_medios_pcp(4)
        valores_aceites = media_para_pedidos(pedidos_total_aceites, pedidos_total_aceites + pedidos_total_rejeitados)
        valores_rejeitados = media_para_pedidos(pedidos_total_rejeitados, pedidos_total_aceites + pedidos_total_rejeitados)
        return render(request,
                  template_name="pedidos_medio_pcp.html",
                  context={'pedidos_medio_aceites':pedidos_total_aceites,'pedidos_medio_rejeitados':pedidos_total_rejeitados,
                           'funcionarios': lista_de_funcionarios, 'valores_a': valores_aceites, 'valores_r': valores_rejeitados})
