import django_filters
from .models import *
from django.db.models import Q


get_estado_choice = [
    ('1', 'Pendente'),
    ('2', 'Em Análise'),
    ('3', 'Aceite'),
    ('4', 'Rejeitado'),
]


get_tipo_choice = [
    ('1', 'Horário'),
    ('2', 'Outros'),
    ('3', 'Sala'),
    ('4', 'Uc'),
] 

def filter_assunto(queryset, name, value):
    for term in value.split():
        queryset = queryset.filter(Q(assunto=term))
    return queryset




class PedidoFilter(django_filters.FilterSet):    
    assunto = django_filters.CharFilter(method=filter_assunto)
    tipo = django_filters.MultipleChoiceFilter(choices=get_tipo_choice)
    estado_0 = django_filters.MultipleChoiceFilter(choices=get_estado_choice)

    class Meta:
        model = Pedido
        fields = '__all__'

