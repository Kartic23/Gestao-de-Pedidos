import django_tables2 as django_tables
from .models import *
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth import *


class PedidosTable(django_tables.Table):

    assunto = django_tables.Column('Assunto')
    informacoes = django_tables.Column('Informações')
    data_de_alvo = django_tables.Column('Data de Alvo')
    data_de_submissao = django_tables.Column('Data de Submissao')
    estado_0 = django_tables.Column('Estado', attrs={"th": {"width": "130"}})
    acoes = django_tables.Column('Ações', empty_values=(),orderable=False, attrs={"th": {"width": "150"}})


    class Meta:
        model = Pedido
        sequence = ('assunto', 'informacoes','data_de_alvo', 'estado_0','data_de_submissao')

    def queryset(self):
        return Pedido.objects.filter(docenteutilizadorid=50)
    
    def before_render(self, request):
        self.columns.hide('id')
        self.columns.hide('anoletivoid')
        self.columns.hide('docenteutilizadorid')
        self.columns.hide('funcionarioutilizadorid')
        self.columns.hide('identificador_id')


    

    def render_tipo(self,value):
        v = ""
        if value.id == 1:
            v = "Horario"
        elif value.id == 2:
            v = "Outros"
        elif value.id == 3:
            v = "Sala"
        elif value.id == 4:
            v = "UC"
        return format_html(f"""
        <span class="tag" style="background-color: orange; font-size: medium;">
        {v}
        </span>
        """)
    
    def render_estado_0(self,value):
        estado = ""
        if value.id == 1:
            estado = "Pendente"
            cor = "aqua"
        elif value.id == 2:
            estado = "Em análise"
            cor = "yellow"
        elif value.id == 3:
            estado = "Aceite"
            cor = "greenyellow"
        elif value.id == 4:
            estado = "Rejeitado"
            cor = "red"
        return format_html(f"""
        <span class="button" style="background-color: {cor}; font-size: medium; min-width: 110px;">
       <strong> {estado}</strong>
        </span>
        """)
    
    def render_data_de_alvo(self,value):
        date_str = str(value)
        parts = date_str.split('-')
        reversed_parts = list(reversed(parts))
        new_date_str = '-'.join(reversed_parts)
        return new_date_str
    


    def render_data_de_submissao(self,value):
        date_str = str(value)
        parts = date_str.split('-')
        reversed_parts = list(reversed(parts))
        new_date_str = '-'.join(reversed_parts)
        return new_date_str
    

    
    def render_data_de_validacao(self,value):
        new_date_str = "____________"
        if value != None:
            datetime_str = str(value)
            date_str = datetime_str.split()[0] # extrai a parte da data
            parts = date_str.split('-')
            reversed_parts = list(reversed(parts))
            new_date_str = '-'.join(reversed_parts)
        return new_date_str



    def render_data_de_associacao(self,value):
        new_date_str = "____________"
        if value != None:
            datetime_str = str(value)
            date_str = datetime_str.split()[0] # extrai a parte da data
            parts = date_str.split('-')
            reversed_parts = list(reversed(parts))
            new_date_str = '-'.join(reversed_parts)
        return new_date_str    
    

    
    def render_acoes(self, record):
        primeiro_botao = """<span class="icon"></span>"""
        segundo_botao = """<span class="icon"></span>"""
        terceiro_botao = """<span class="icon"></span>"""
        quarto_botao = """<span class="icon"></span>"""

        user = get_user(self.request)
        if record.tipo.id == 1:
            primeiro_botao = f"""
                    <a data-tooltip="Consultar" href="consultarpedidohorario/{record.id}">
                        <span class="icon">
                            <i class="mdi mdi-eye mdi-24px" style="color: #32CD32"></i>
                        </span>
                    </a>
                    """
        elif record.tipo.id == 2:   
            primeiro_botao = f"""
                    <a data-tooltip="Consultar" href="consultarpedidooutros/{record.id}">
                        <span class="icon">
                            <i class="mdi mdi-eye mdi-24px" style="color: #32CD32"></i>
                        </span>
                    </a>
                    """
        elif record.tipo.id == 3:
            primeiro_botao = f"""
                    <a data-tooltip="Consultar" href="consultarpedidosala/{record.id}">
                        <span class="icon">
                            <i class="mdi mdi-eye mdi-24px" style="color: #32CD32"></i>
                        </span>
                    </a>
                    """
        elif record.tipo.id == 4:
            primeiro_botao = f"""
                    <a data-tooltip="Consultar" href="consultarpedidosuc/{record.id}">
                        <span class="icon">
                            <i class="mdi mdi-eye mdi-24px" style="color: #32CD32" ></i>
                        </span>
                    </a>
                    """
            
            
        if user.groups.filter(name = "Docente").exists():
            if record.estado_0.id == 1:
                if record.tipo.id == 1:
                    segundo_botao = f""" <a  data-tooltip="Editar" href="editarpedidohorario/{record.id}"  class="icon">
                        <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                    </a>
                    """
                    terceiro_botao = f"""<a data-tooltip="Eliminar" href="eliminarpedidohorario/{record.id}" class="icon has-text-danger" >
                        <i class="mdi mdi-trash-can mdi-24px"></i>
                    </a>
                    """
                elif record.tipo.id == 2:
                    segundo_botao = f""" <a  data-tooltip="Editar" href="editarpedidooutros/{record.id}"  class="icon">
                        <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                    </a>
                    """
                    terceiro_botao = f"""<a data-tooltip="Eliminar" href="eliminarpedidooutros/{record.id}" class="icon has-text-danger" >
                        <i class="mdi mdi-trash-can mdi-24px"></i>
                    </a>
                    """
                elif record.tipo.id == 3:
                    segundo_botao = f""" <a data-tooltip="Editar" href="editarpedidosala/{record.id}"  class="icon">
                        <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                    </a>
                    """
                    terceiro_botao = f"""<a data-tooltip="Eliminar" href="eliminarpedidosala/{record.id}" class="icon has-text-danger" >
                        <i class="mdi mdi-trash-can mdi-24px"></i>
                    </a>
                    """
                elif record.tipo.id == 4:
                    segundo_botao = f""" <a data-tooltip="Editar" href="editarpedidouc/{record.id}"  class="icon">
                        <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                    </a>
                    """
                    terceiro_botao = f"""<a  data-tooltip="Eliminar" href="eliminarpedidouc/{record.id}" class="icon has-text-danger" >
                        <i class="mdi mdi-trash-can mdi-24px"></i>
                    </a>
                    """
        elif user.groups.filter(name="Funcionario").exists():
                if record.estado_0.id == 1:
                     segundo_botao = f"""
                            <a data-tooltip="Associar" href="associarpedidofuncionario/{record.id}">
                                <span class="icon">
                                    <i class="mdi mdi-circle-edit-outline mdi-24px" style="color: orange"></i>
                                </span>
                            </a>
                            """
                if record.estado_0.id == 2  and user.id == record.funcionarioutilizadorid.id :
                    segundo_botao = f"""
                            <a data-tooltip="Validar" href="validarpedido/{record.id}">
                                <span class="icon">
                                    <i class="fas fa-check " style="color: #32CD32"></i>
                                </span>
                            </a>
                            """
                    terceiro_botao = f"""
                            <a data-tooltip="Desassociar" href="desassociarpedidofuncionario/{record.id}">
                                <span class="icon">
                                    <i class="mdi mdi-circle-edit-outline mdi-24px" style="color: red"></i>
                                </span>
                            </a>
                            """
                quarto_botao = f"""
                            <a data-tooltip="Obter Informação PCP" href="obterinformacao/{record.id}">
                                <span class="icon">
                                    <i class="mdi mdi-help mdi-24px" style="color: rgb(0,0,0) "></i>
                                </span>
                            </a>
                            """

                   
        return format_html(f"""
        <div>
            {primeiro_botao}
            {segundo_botao}
            {terceiro_botao}
            {quarto_botao}
        </div>
        """)
    

class ExportarPedidosTable(django_tables.Table):

    assunto = django_tables.Column('Assunto')
    informacoes = django_tables.Column('Informações')
    data_de_alvo = django_tables.Column('Data de Alvo')
    data_de_submissao = django_tables.Column('Data de Submissao')
    estado_0 = django_tables.Column('Estado', attrs={"th": {"width": "130"}})
    acoes = django_tables.Column('Ações', empty_values=(),orderable=False, attrs={"th": {"width": "150"}})


    class Meta:
        model = Pedido
        sequence = ('assunto', 'informacoes','data_de_alvo', 'estado_0','data_de_submissao')

    def queryset(self):
        return Pedido.objects.filter(docenteutilizadorid=50)
    
    def before_render(self, request):
        self.columns.hide('id')
        self.columns.hide('anoletivoid')
        self.columns.hide('docenteutilizadorid')
        self.columns.hide('funcionarioutilizadorid')
        self.columns.hide('identificador_id')


    

    def render_tipo(self,value):
        v = ""
        if value.id == 1:
            v = "Horario"
        elif value.id == 2:
            v = "Outros"
        elif value.id == 3:
            v = "Sala"
        elif value.id == 4:
            v = "UC"
        return format_html(f"""
        <span class="tag" style="background-color: orange; font-size: medium;">
        {v}
        </span>
        """)
    
    def render_estado_0(self,value):
        estado = ""
        if value.id == 1:
            estado = "Pendente"
            cor = "aqua"
        elif value.id == 2:
            estado = "Em análise"
            cor = "yellow"
        elif value.id == 3:
            estado = "Aceite"
            cor = "greenyellow"
        elif value.id == 4:
            estado = "Rejeitado"
            cor = "red"
        return format_html(f"""
        <span class="button" style="background-color: {cor}; font-size: medium; min-width: 110px;">
       <strong> {estado}</strong>
        </span>
        """)
    
    def render_data_de_alvo(self,value):
        date_str = str(value)
        parts = date_str.split('-')
        reversed_parts = list(reversed(parts))
        new_date_str = '-'.join(reversed_parts)
        return new_date_str
    


    def render_data_de_submissao(self,value):
        date_str = str(value)
        parts = date_str.split('-')
        reversed_parts = list(reversed(parts))
        new_date_str = '-'.join(reversed_parts)
        return new_date_str
    

    
    def render_data_de_validacao(self,value):
        new_date_str = "____________"
        if value != None:
            datetime_str = str(value)
            date_str = datetime_str.split()[0] # extrai a parte da data
            parts = date_str.split('-')
            reversed_parts = list(reversed(parts))
            new_date_str = '-'.join(reversed_parts)
        return new_date_str



    def render_data_de_associacao(self,value):
        new_date_str = "____________"
        if value != None:
            datetime_str = str(value)
            date_str = datetime_str.split()[0] # extrai a parte da data
            parts = date_str.split('-')
            reversed_parts = list(reversed(parts))
            new_date_str = '-'.join(reversed_parts)
        return new_date_str    
    

    
    def render_acoes(self, record):
        primeiro_botao = """<span class="icon"></span>"""
        segundo_botao = """<span class="icon"></span>"""
        terceiro_botao = """<span class="icon"></span>"""
        user = get_user(self.request)
        primeiro_botao = f"""
        """
        segundo_botao = f"""
            <a data-tooltip="Exportar CSV" href="exportarpedidoscsv/{record.id}">
                <span class="icon">
                    <i class="fas fa-check " style="color: #32CD32"></i>
               </span>
            </a>
           """
        terceiro_botao = f"""
            <a data-tooltip="Exportar PDF" href="exportarpedidosfuncionario/{record.id}">
                <span class="icon">
                    <i class="mdi mdi-circle-edit-outline mdi-24px" style="color: red"></i>
                </span>
            </a>
           """
                   
        return format_html(f"""
        <div>
            {primeiro_botao}
            {segundo_botao}
            {terceiro_botao}
        </div>
        """)