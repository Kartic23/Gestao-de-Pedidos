"""gestaopedidos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import homepage
from .views import escolher_perfil
from .views import criar_utilizador
from .views import login_action,logout_action
from .views import concluir_registo_utilizador
from .views import mensagem

app_name = "main"

urlpatterns = [
    path("", homepage, name="homepage"),
    path('escolherperfil', escolher_perfil,name='escolher-perfil'),  
    path('criarutilizadores/<int:id>', criar_utilizador, name='criar-utilizador'),
    path('login', login_action,name="login"),
    path('concluirregistoutilizador/<int:id>',concluir_registo_utilizador, name='concluir-registo-utilizador' ),
    path('mensagem/<int:id>', mensagem,name='mensagem'),
    path("logout", logout_action, name="logout"), 
]

