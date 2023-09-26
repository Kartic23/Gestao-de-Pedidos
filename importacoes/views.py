from django.shortcuts import render
from django.shortcuts import render, HttpResponse
import xlrd
from main.models import *
from pedidos.models import *
from anoletivo.models import *
from .models import *
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.views.generic.list import *
from django.http import HttpResponse
from django.contrib.auth import *
import pandas as pd
from django.http import HttpResponse
from datetime import datetime

def importar(request):
    return render(request,
                  template_name="importar.html",
                  )

def importar_ruc(request):
    if request.method == 'POST' and 'arquivo' in request.FILES:
        arquivo = request.FILES['arquivo']
        if str(arquivo).endswith(".xls"):
            if arquivo:
                conteudo = arquivo.read()
                workbook = xlrd.open_workbook(file_contents=conteudo)
                worksheet = workbook.sheet_by_index(0)
                if worksheet.cell_value(0, 0) == "&#160;" and worksheet.cell_value(0, 1) == "Ano letivo" and worksheet.cell_value(0, 2) == "Docente"  and worksheet.cell_value(0, 3) == "Regência":
                    linhas = conteudo.splitlines()
                    dados_do_excel_UC =[]
                    dados_do_excel_Curso =[]
                    dados_do_excel_Departamento =[]
                    for row in range(1, min(worksheet.nrows, len(linhas))):  
                        ano = worksheet.cell_value(row, 1)
                        ano_formatado =""                                #ano letivo no formato nnnn/nn
                        for i in range(0,len(ano)):
                            if ano[i] == '-':
                                ano_formatado = ano_formatado + "/"
                            else:
                                ano_formatado = ano_formatado + ano[i]     

                        
                        docente = worksheet.cell_value(row, 2)
                        docente_codigo = docente.split("-")[0].strip()    #Codigo do Docente
                        docente_nome = docente.split("-")[1].strip()      #Nome do Docente
                        docentes = Docente.objects.filter(codigo=docente_codigo).first()
                        if docentes:
                            docente_id = docentes.id
                            estado_docente = "S"
                        else:
                            docente_email = 'd' + docente_codigo +'@ualg.pt'
                            docente_username = 'd' + docente_codigo
                            docente = Docente.objects.create(codigo=docente_codigo,username=docente_username, email=docente_email, password=(docente_codigo+"123#"))
                            docente.nome = docente_nome
                            docente.save()
                            docente_id = docente.id
                            estado_docente = "N"

                        regencia = worksheet.cell_value(row, 3)
                        tipo =  worksheet.cell_value(row, 4)
                        tipo_regencia = ""
                        t = False
                        for i in range(0,len(tipo)):
                            if tipo[i] == ')':
                                t = False
                            if t == True:
                                tipo_regencia += tipo[i]
                            if tipo[i] == '(':
                                t = True

                        tipo_regencia_id = TipoDeRegencia.objects.get(tipo=tipo_regencia).id
                        if tipo_regencia == "Disciplina":
                            t = False
                            uc_codigo = "" 
                            if regencia.split("(")[1].strip()[2].isdigit():
                                for i in range(0,len(regencia)):
                                    if regencia[i] == ')':
                                        t = False
                                    if t == True:
                                        uc_codigo += regencia[i]
                                    if regencia[i] == '(':
                                        t = True
                            else:
                                uc_codigo = regencia.split("(")[2].strip()
                                uc_codigo = uc_codigo.split(")")[0].strip()
                                
                            uc_nome = regencia.split("(")[0].strip() 
                            ucs = Uc.objects.filter(codigo=uc_codigo).first()
                            if ucs:
                                uc_id = ucs.id
                                estado_UC = "S"
                            else:
                                new_Uc = Uc(codigo=uc_codigo,disciplina=uc_nome)
                                new_Uc.save()
                                uc_id = new_Uc.id
                                estado_UC = "N"

                            
                            check_regencia = Regencia.objects.filter(ano_letivo_id=ano_letivo.objects.get(ano_letivo=ano_formatado).id,
                                    docente_id=Docente.objects.get(user_ptr_id=docente_id).id,
                                    tipo_regencia_id=TipoDeRegencia.objects.get(tipo=tipo_regencia).id,
                                    regencia_id=uc_id).first()
                            if check_regencia:
                                estado_Regencia = "S"
                            else:
                                new_regencia = Regencia(
                                        ano_letivo_id=ano_letivo.objects.get(ano_letivo=ano_formatado),
                                        docente_id=Docente.objects.get(user_ptr_id=docente_id),
                                        tipo_regencia_id=TipoDeRegencia.objects.get(tipo=tipo_regencia),
                                        regencia_id=uc_id)
                                new_regencia.save()
                                estado_Regencia = "N"
                            linha = {
                                "ano_letivo": ano_formatado,
                                "tipo_regencia": tipo_regencia,
                                "tipo_regencia_id": tipo_regencia_id,
                                "docente_id": docente_id,
                                "nome_docente": docente_nome,
                                "codigo_docente": docente_codigo,
                                "new_docente": estado_docente,
                                "uc" : uc_nome,
                                "uc_codigo": uc_codigo,
                                "new_uc": estado_UC,
                                "new_Regencia": estado_Regencia
                            }
                            dados_do_excel_UC.append(linha)

                        elif tipo_regencia == "Curso":
                            curso_nome = regencia.split("(")[0].strip() 
                            curso_ciclo = regencia.split("(")[1].strip()[0]
                            curso_codigo = regencia.split("(")[2].strip()
                            curso_codigo = curso_codigo.split(")")[0].strip()

                            curso_check = Curso.objects.filter(codigo=curso_codigo).first()
                            if curso_check:
                                curso_id = curso_check.id
                                estado_curso = "S"
                            else:
                                new_curso = Curso.objects.create(curso_nome=curso_nome,ciclo=curso_ciclo,codigo=curso_codigo)
                                curso_id = new_curso.id
                                estado_curso = "N"

                            check_regencia = Regencia.objects.filter(ano_letivo_id=ano_letivo.objects.get(ano_letivo=ano_formatado).id,
                                    docente_id=Docente.objects.get(user_ptr_id=docente_id).id,
                                    tipo_regencia_id=TipoDeRegencia.objects.get(tipo=tipo_regencia).id,
                                    regencia_id=curso_id).first()
                            if check_regencia:
                                estado_Regencia = "S"
                            else:
                                new_regencia = Regencia(
                                        ano_letivo_id=ano_letivo.objects.get(ano_letivo=ano_formatado),
                                        docente_id=Docente.objects.get(user_ptr_id=docente_id),
                                        tipo_regencia_id=TipoDeRegencia.objects.get(tipo=tipo_regencia),
                                        regencia_id=curso_id)
                                new_regencia.save()
                                estado_Regencia = "N"

                            linha = {
                                "ano_letivo": ano_formatado,
                                "tipo_regencia": tipo_regencia,
                                "tipo_regencia_id": tipo_regencia_id,
                                "docente_id": docente_id,
                                "nome_docente": docente_nome,
                                "codigo_docente": docente_codigo,
                                "new_docente": estado_docente,
                                "curso" : curso_nome,
                                "new_curso": estado_curso,
                                "new_Regencia": estado_Regencia
                            }
                            dados_do_excel_Curso.append(linha)

                        elif tipo_regencia == "Departamento":
                            departamento = regencia.split("(")[0].strip() 
                            departamento_check = Departamento.objects.filter(nome=departamento).first()
                            if departamento_check:
                                departamento_id = departamento_check.id
                                estado_Dep = "N"
                            else:
                                estado_Dep = "S"

                            check_regencia = Regencia.objects.filter(ano_letivo_id=ano_letivo.objects.get(ano_letivo=ano_formatado).id,
                                    docente_id=Docente.objects.get(user_ptr_id=docente_id).id,
                                    tipo_regencia_id=TipoDeRegencia.objects.get(tipo=tipo_regencia).id,
                                    regencia_id=departamento_id).first()
                            if check_regencia:
                                estado_Regencia = "S"
                            else:
                                new_regencia = Regencia(
                                        ano_letivo_id=ano_letivo.objects.get(ano_letivo=ano_formatado),
                                        docente_id=Docente.objects.get(user_ptr_id=docente_id),
                                        tipo_regencia_id=TipoDeRegencia.objects.get(tipo=tipo_regencia),
                                        regencia_id=departamento_id)
                                new_regencia.save()
                                estado_Regencia = "N"
                            
                            linha = {
                                "ano_letivo": ano_formatado,
                                "tipo_regencia": tipo_regencia,
                                "tipo_regencia_id": tipo_regencia_id,
                                "docente_id": docente_id,
                                "nome_docente": docente_nome,
                                "codigo_docente": docente_codigo,
                                "new_docente": estado_docente,
                                "dep" : departamento,
                                "new_Dep": estado_Dep,
                                "new_Regencia": estado_Regencia
                            }
                            dados_do_excel_Departamento.append(linha)
                    
                    return render(request,
                        template_name="listagem_dados_RUC_importados.html",
                        context={'Ucs' : dados_do_excel_UC, 'Deps': dados_do_excel_Departamento,'Curso':dados_do_excel_Curso})
                else:
                    return redirect('main:mensagem',21)

        else:
            return redirect('main:mensagem',20)


    else:
        return render(request,
                  template_name="importar_RUC.html")
    
def importar_docente(request):
    if request.method == 'POST' and 'arquivo' in request.FILES:
        arquivo = request.FILES['arquivo']
        if str(arquivo).endswith(".xls"):
            if arquivo:
                conteudo = arquivo.read()
                workbook = xlrd.open_workbook(file_contents=conteudo)
                worksheet = workbook.sheet_by_index(0)
                if worksheet.cell_value(0, 0) == "&#160;" and worksheet.cell_value(0, 1) == "Código" and worksheet.cell_value(0, 2) == "Docente"  and worksheet.cell_value(0, 3) == "Ativo":
                    linhas = conteudo.splitlines()
                    dados_do_excel_Docente =[]
                    for row in range(1, min(worksheet.nrows, len(linhas))):  
                        docente_codigo = int(worksheet.cell_value(row, 1))    
                        docente = worksheet.cell_value(row, 2)
                        ativo = worksheet.cell_value(row, 3)
                        docente_nome  =  worksheet.cell_value(row, 4)
                        individuo = worksheet.cell_value(row, 5)
                        data_de_nascimento = worksheet.cell_value(row, 6)
                        sexo = worksheet.cell_value(row, 7)
                        tipo_de_identificacao = worksheet.cell_value(row, 8)
                        identificacao = worksheet.cell_value(row, 9)
                        data_de_emissao_da_identificacao = worksheet.cell_value(row, 10)
                        nacionalidade = worksheet.cell_value(row, 11)
                        docente_arquivo = worksheet.cell_value(row, 12)
                        data_de_validade_da_identificacao = worksheet.cell_value(row, 13)
                        Nif = worksheet.cell_value(row, 14)
                        pais_fiscal = str(worksheet.cell_value(row, 15))
                        if len(pais_fiscal) == 0:
                            pais_fiscal = "0"
                        digito_verificacao = str(worksheet.cell_value(row, 16))
                        if len(digito_verificacao) == 0:
                            digito_verificacao = "0"
                        docentes = Docente.objects.filter(codigo=docente_codigo).first()
                        if docentes:
                            estado_docente = "S"
                        else:
                            docente_email = 'd' + str(docente_codigo) +'@ualg.pt'
                            docente_username = 'd' + str(docente_codigo)
                            docente_pass = str(docente_codigo)+"123#"
                            docente_ative = False
                            docente = Docente.objects.create(codigo=docente_codigo,username=docente_username, email=docente_email, password=docente_pass,is_active=docente_ative)
                            docente.ano_letivoid = ano_letivo.objects.get(ativo="S").id
                            docente.nome = docente_nome
                            docente.ativo = ativo
                            docente.individuo = individuo
                            docente.data_de_nascimento = "1990-01-25"
                            docente.sexo = sexo
                            docente.tipo_de_identificacao = tipo_de_identificacao
                            docente.identificacao = identificacao
                            docente.data_de_emissao_da_identificacao = data_de_emissao_da_identificacao
                            docente.nacionalidade = nacionalidade
                            docente.docente_arquivo = docente_arquivo
                            docente.data_de_validade_da_identificacao = data_de_validade_da_identificacao
                            docente.nif = Nif
                            docente.pais_fiscal = float(pais_fiscal)
                            docente.digito_verificacao = float(digito_verificacao)
                            docente.save()
                            estado_docente = "N"
                        linha = {
                            "nome_docente": docente_nome,
                            "codigo_docente": docente_codigo,
                            "new_Doc": estado_docente
                        }
                        dados_do_excel_Docente.append(linha)
                    return render(request,
                        template_name="listagem_dados_docente_importados.html",
                        context={'Docentes' : dados_do_excel_Docente})
                else:
                    return redirect('main:mensagem',23)

        else:
            return redirect('main:mensagem',20)
        
    else:
        return render(request,
                  template_name="importar_docente.html")






def importar_dsd(request):
    if request.method == 'POST' and 'arquivo' in request.FILES:
        arquivo = request.FILES['arquivo']
        if str(arquivo).endswith(".xls"):
            if arquivo:
                conteudo = arquivo.read()
                workbook = xlrd.open_workbook(file_contents=conteudo)
                worksheet = workbook.sheet_by_index(0)
                if worksheet.cell_value(0, 0) == "Período" and worksheet.cell_value(0, 1) == "Cód. disciplina" and worksheet.cell_value(0, 2) == "Disciplina"  and worksheet.cell_value(0, 3) == "Inst. discip.":
                    linhas = conteudo.splitlines()
                    dados_do_excel_UC =[]
                    dados_do_excel_Departamento =[]
                    for row in range(1, min(worksheet.nrows, len(linhas))):
                        disciplina_periodo = worksheet.cell_value(row, 0)
                        disciplina_codigo = worksheet.cell_value(row, 1)     
                        disciplina_nome = worksheet.cell_value(row, 2)
                        disciplina_inst_disc = worksheet.cell_value(row, 3)
                        disciplina_inst_disciplina = worksheet.cell_value(row, 4)
                        disciplina_depart = worksheet.cell_value(row, 5)
                        disciplina_turma = worksheet.cell_value(row, 6)
                        disciplina_curso_codigo = str(worksheet.cell_value(row, 7))
                        if len(disciplina_curso_codigo) == 0:
                            disciplina_curso_codigo = "0"
                        disciplina_curso = worksheet.cell_value(row, 8)
                        docente_codigo = worksheet.cell_value(row, 9)
                        docente_d = worksheet.cell_value(row, 10)
                        docente_funcao = worksheet.cell_value(row, 11)
                        docente_inst = worksheet.cell_value(row, 12)
                        docente_depart = worksheet.cell_value(row, 13)

                        disciplina_horas_semanais = worksheet.cell_value(row, 14)
                        horas_semanas, minutos_semanas = disciplina_horas_semanais.split(':')

                        disciplina_horas_periodo = worksheet.cell_value(row, 15)
                        horas_periodo, minutos_periodo = disciplina_horas_semanais.split(':')


                        disciplina_factor = worksheet.cell_value(row, 16)
                        disciplina_horas_serviço = worksheet.cell_value(row, 17)

                        disciplina_data_inicio = worksheet.cell_value(row, 18)
                        data_i = datetime.strptime(disciplina_data_inicio, '%d/%m/%Y')
                        data_i = data_i.strftime('%Y-%m-%d')

                        disciplina_data_fim = worksheet.cell_value(row, 19)
                        data_f = datetime.strptime(disciplina_data_fim, '%d/%m/%Y')
                        data_f = data_f.strftime('%Y-%m-%d')

                        docente_nome = worksheet.cell_value(row, 20)
                        disciplina_agrupamento = worksheet.cell_value(row, 21)
                        docentes = Docente.objects.filter(codigo=docente_codigo).first()
                        if docentes:
                            docente_id = docentes.id
                            estado_docente = "S"
                        else:
                            docente_email = 'd' + str(docente_codigo) +'@ualg.pt'
                            docente_username = 'd' + str(docente_codigo)
                            docente_password = str(docente_codigo)+"123#"
                            docente = Docente.objects.create(codigo=docente_codigo,username=docente_username, email=docente_email, password=docente_password)
                            docente.nome = docente_nome
                            docente.save()
                            docente_id = docente.id
                            estado_docente = "N"

                        #uc = Uc.objects.get(codigo = disciplina_codigo)
                        #if (uc.turma != disciplina_turma or uc.curso != disciplina_curso):
                        check_uc = Uc.objects.filter(period = disciplina_periodo, 
                                                    disciplina = disciplina_nome, 
                                                    inst_discip = disciplina_inst_disc, 
                                                    inst_disciplina_full = disciplina_inst_disciplina, 
                                                    depart_disciplina = disciplina_depart, 
                                                    turma = disciplina_turma, 
                                                    codigo_curso = float(disciplina_curso_codigo), 
                                                    curso = disciplina_curso, 
                                                    horas_semanais = horas_semanas, 
                                                    horas_periodo = horas_periodo, 
                                                    horas_servico = disciplina_horas_serviço, 
                                                    data_inicio = data_i, 
                                                    data_fim = data_f
                                                    ).first()
                        if not check_uc:
                            uniC = Uc.objects.create(codigo=disciplina_codigo,period = disciplina_periodo,disciplina = disciplina_nome,inst_discip = disciplina_inst_disc,inst_disciplina_full = disciplina_inst_disciplina,depart_disciplina = disciplina_depart,turma = disciplina_turma,codigo_curso = float(disciplina_curso_codigo),curso = disciplina_curso,horas_semanais = horas_semanas,horas_periodo = horas_periodo,horas_servico = disciplina_horas_serviço,data_inicio = data_i,data_fim = data_f)
                            unic_id = uniC.id
                        
                        else:
                            unic_id = check_uc.id
                        linha = {
                            "Disciplina": disciplina_nome,
                            "Instituto": disciplina_inst_disc,
                            "Turma": disciplina_turma,
                            "Docente": docente_nome,
                        }
                        docente_uc = DocenteUc()
                        docente_uc.docenteutilizadorid = Docente.objects.get(user_ptr = docente_id)
                        docente_uc.ucid = Uc.objects.get(id = unic_id)
                        docente_uc.save()
                        dados_do_excel_UC.append(linha)
                    
                    return render(request,
                        template_name="listagem_dados_dsd_importados.html",
                        context={'Ucs' : dados_do_excel_UC})
                else:
                    return redirect('main:mensagem',21)

        else:
            return redirect('main:mensagem',20)


    else:
        return render(request,
                  template_name="importar_dsd.html")
    




def importar_sala(request):
    if request.method == 'POST' and 'arquivo' in request.FILES:
        arquivo = request.FILES['arquivo']
        if str(arquivo).endswith(".xls"):
            if arquivo:
                conteudo = arquivo.read()
                workbook = xlrd.open_workbook(file_contents=conteudo)
                worksheet = workbook.sheet_by_index(0)
                print(worksheet.cell_value(0, 0))
                print(worksheet.cell_value(0, 1))
                print(worksheet.cell_value(0, 2))
                print(worksheet.cell_value(0, 3))
                print(worksheet.cell_value(0, 4))
                print(worksheet.cell_value(0, 5))
                print("-------------------------------------")
                
                if worksheet.cell_value(0, 0) == "Nome Instituição" and worksheet.cell_value(0, 1) == "Desc. Edifício"  and worksheet.cell_value(0, 2) == "Desc. Sala" and worksheet.cell_value(0, 3) == "Des. Categoria" and worksheet.cell_value(0, 4) == "Id. tipo sala" and worksheet.cell_value(0, 5) == "Lotação presencial sala":
                    linhas = conteudo.splitlines()
                    
                    dados_do_excel_Sala =[]


                       

                    for row in range(1, min(worksheet.nrows, len(linhas))):  
                        print(worksheet.cell_value(row, 0))
                        print("E: " + worksheet.cell_value(row, 1))
                        print(worksheet.cell_value(row, 2))
                        print(worksheet.cell_value(row, 3))
                        print(worksheet.cell_value(row, 4))
                        print(worksheet.cell_value(row, 5))



                        Nome_Instituição = Instituicao.objects.get(nome_instituicao=worksheet.cell_value(row, 0)).id

                        Desc_Edifício = Edificio.objects.get(edificio=worksheet.cell_value(row, 1)).id

                        Desc_Sala = worksheet.cell_value(row, 2)

                        
                        cts = Categoria.objects.all();
                        for c in cts:
                            if(str(c.tipo_de_sala).split("\r\n")[0] == str(worksheet.cell_value(row,3))):
                               Des_Categoria = c.id
                               break

                        cts = TipoDeAulas.objects.all();
                        for c in cts:
                            if(str(c.tipo_aula).split("\r\n")[0] ==  str(worksheet.cell_value(row, 4))):
                               print("Entrou:  " + str(c.tipo_aula) + " id: " + str(c.id))
                               Id_tipo_sala = c.id
                               break


                        


                

                        Lotação_presencial_sala = int(worksheet.cell_value(row, 5))

                        if(Lotação_presencial_sala < 0):
                            Lotação_presencial_sala=0

                            
                        
  



                        check_sala = Sala.objects.filter(descricao_sala=Desc_Sala).first()
                        if check_sala:
                                estado_sala = "S"
                        else:
                            new_Sala = Sala(
                                        id_nome_instituicao=Nome_Instituição,
                                        id_nome_edificio=Desc_Edifício,
                                        descricao_sala=Desc_Sala,
                                        id_tipo_aula=Id_tipo_sala,
                                        id_nome_tipo_sala=Des_Categoria,
                                        lotacao=Lotação_presencial_sala,
                                        id_estado_da_sala=1,
                                        id_ano_letivo=ano_letivo.objects.get(ativo="S").id)
                            new_Sala.save()
                            estado_sala = "N"

                        linha = {
                                "Nome_Instituição": worksheet.cell_value(row, 0),
                                "Desc_Edifício": worksheet.cell_value(row, 1),
                                "Desc_Sala": Desc_Sala,
                                "Des_Categoria": worksheet.cell_value(row,3),
                                "Id_tipo_sala": worksheet.cell_value(row,4),
                                "Lotação_presencial_sala": Lotação_presencial_sala,
                                "new_sala":estado_sala
                        }
                        
                        dados_do_excel_Sala.append(linha)

                    
                    return render(request,
                        template_name="listagem_dados_SALA_importados.html",
                        context={'dados' : dados_do_excel_Sala})
                else:
                    return redirect('main:mensagem',21)

        else:
            return redirect('main:mensagem',20)


    else:
        return render(request,
                  template_name="importar_SALA.html")
