from . import views
from django.urls import path
from django.urls import re_path as pattern


app_name = 'notificacoes'

urlpatterns = [

    path('detalhes/<int:id>', views.sem_notificacoes,
         name='sem-notificacoes'),

    path('limpar/<int:id>', views.limpar_notificacoes,
         name='limpar-notificacoes'),
    path('marcarcomolida', views.marcar_como_lida,
         name='ler-notificacoes'),

    ################################ Mensagens ###########################

    path('escolhertipo', views.escolher_tipo, name="enviar-notificacao"),
    path('criarmensagem/<int:id>', views.criar_mensagem, name="escrever-mensagem"),
    path('criarmensagemparticipante/<int:id>',
         views.criar_mensagem_participante, name="criar-mensagem-participante"),
    path('mensagens/<int:id>', views.sem_mensagens,
         name='sem-mensagens'),
    path('concluirenvio', views.concluir_envio,
         name='concluir-envio'),
    path('mensagens/<int:id>/<int:nr>', views.detalhes_mensagens,
         name='detalhes-mensagem'),
    path('apagarmensagem/<int:id>/<int:nr>', views.apagar_mensagem,
         name='apagar-mensagem'),
    path('limparmensganes/<int:id>', views.limpar_mensagens,
         name='limpar-mensagens'),
    path('marcarmensagemcomolida/<int:id>', views.mensagem_como_lida,
         name='ler-mensagens'),
]
