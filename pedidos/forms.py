from django.forms import *
from django import forms
from .models import *


class PedidoOutrosForm(forms.ModelForm):
    data = forms.CharField(max_length=25)
    assunto = forms.CharField(max_length=255)
    subpedidos = forms.CharField(widget=forms.HiddenInput(), required=False)
    informacoes = forms.CharField(max_length=500)


    class Meta:
        model = PedidoOutros
        fields = ('data','assunto', 'subpedidos','informacoes',)
    
    def clean(self) :
        data = self.cleaned_data.get('data')
        assunto = self.cleaned_data.get('assunto')



class PedidoHorarioForm(forms.ModelForm):
    assunto = forms.CharField(max_length=255)
    data = forms.CharField(max_length=255)
    subpedidos = forms.CharField(widget=forms.HiddenInput(), required=False)
    descricao = forms.CharField(max_length=500)


    class Meta:
        model = PedidoDeHorario
        fields = ('assunto', 'data', 'subpedidos', 'descricao',)
    
    def clean(self) :
        hora_inicial = self.cleaned_data.get('hora_inicial')
        hora_final = self.cleaned_data.get('hora_final')
        assunto = self.cleaned_data.get('assunto')
        data = self.cleaned_data.get('data')
        descricao = self.cleaned_data.get('descricao')



class PedidoSalasForm(forms.ModelForm):
    data = forms.CharField(max_length=25)
    assunto = forms.CharField(max_length=255)
    subpedidos = forms.CharField(widget=forms.HiddenInput(), required=False)
    informacoes = forms.CharField(max_length=500)

    class Meta:
        model = PedidoDeSala
        fields = ('data','assunto', 'subpedidos','informacoes',)
    
    def clean(self) :
        data = self.cleaned_data.get('data')
        assunto = self.cleaned_data.get('assunto')

        

class PedidoUcForm(forms.ModelForm):
    descricao = forms.CharField(max_length=500)
    data = forms.CharField(max_length=100)
    assunto = forms.CharField(max_length=100)

    class Meta:
        model = PedidoUc
        fields = ('descricao','data','assunto',)
    
    def clean(self) :
        descricao = self.cleaned_data.get('descricao')
        data = self.cleaned_data.get('data')
        assunto = self.cleaned_data.get('assunto')
