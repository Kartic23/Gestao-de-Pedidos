from django.urls import path
from .views import importar,importar_ruc, importar_docente
from .views import importar_sala, importar_dsd

app_name = "importacoes"

urlpatterns = [
    
    path('importar', importar, name='importar'),
    path('importarruc', importar_ruc, name='importar-ruc'),
    path('importardocente', importar_docente, name='importar-docente'),
    path('importarsala', importar_sala, name='importar-sala'),
    path('importardsd', importar_dsd, name='importar-dsd'),
]

