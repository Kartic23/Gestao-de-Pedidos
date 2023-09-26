from django.urls import path
from .views import criar_ano_letivo,consultar_ano_letivo,eliminar_ano_letivo,ativar_desativar_ano_letivo
from .views import mensagem


app_name = "anoletivo"

urlpatterns = [
    path('criaranoletivo', criar_ano_letivo, name='criar-ano-letivo'),
    path('eliminaranoletivo/<int:id>', eliminar_ano_letivo, name='eliminar-ano-letivo'),
    path('consultaranoletivo', consultar_ano_letivo, name='consultar-ano-letivo'),
    path('ativardesativaranoletivo/<int:id>', ativar_desativar_ano_letivo, name='ativar-desativar-ano-letivo'),
    path('mensagem/<int:id>', mensagem,name='mensagem'),
]

