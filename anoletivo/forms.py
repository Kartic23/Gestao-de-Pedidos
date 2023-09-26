from django.forms import *
from django import forms
from .models import *

class AnoLetivoForm(forms.ModelForm):
    ano_letivo = forms.CharField(max_length=255)
    dia_inicio = forms.CharField(max_length=25)
    dia_fim =  forms.CharField(max_length=25)

    class Meta:
        model = ano_letivo
        fields = ('ano_letivo','dia_inicio','dia_fim',)