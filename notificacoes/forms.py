from django.forms import ModelForm

from main.models import Funcionario
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,PasswordChangeForm
from django.forms import *
from django.contrib.auth.models import User
from django import forms

from main.models import *



USER_CHOICES = (
    ("Docente", "Docente"),
    ("Funcionario", "Funcionario"),
    ("PCP", "PCP"),
)

class UtilizadorFiltro(Form):
    filtro_tipo = ChoiceField(
        choices=USER_CHOICES,
        widget=Select(),
        required=True,
    )



USER_CHOICES_PARTICIPANTE = (
    ("Administrador", "Administrador"),
)

class UtilizadorFiltroParticipante(Form):
    filtro_tipo = ChoiceField(
        choices=USER_CHOICES_PARTICIPANTE,
        widget=Select(),
        required=True,
    )


USER_CHOICES_UO = (
    ("Docente", "Docente"),
    ("Funcionario", "Funcionario"),
    ("PCP", "PCP"),
)

class UtilizadorFiltroUO(Form):
    filtro_tipo = ChoiceField(
        choices=USER_CHOICES_UO,
        widget=Select(),
        required=True,
    )

class MensagemFormIndividualAdmin(forms.Form):
    email = CharField(widget=TextInput(), max_length=255, required=False)
    titulo = CharField(widget=TextInput(), max_length=255, required=False)
    mensagem = CharField(widget=forms.Textarea, max_length=255, required=False)
    def clean(self):
        email = self.cleaned_data.get('email')
        titulo = self.cleaned_data.get('titulo')
        mensagem = self.cleaned_data.get('mensagem')
        # email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError(f'Este email não é válido!')
        if email == "" or titulo=="" or mensagem=="":
            raise forms.ValidationError(f'Todos os campos são obrigatórios!')


class MensagemFormGrupoAdmin(forms.Form):
    titulo = CharField(widget=TextInput(), max_length=255, required=False)
    mensagem = CharField(widget=forms.Textarea, max_length=255, required=False)
    def clean(self):
        titulo = self.cleaned_data.get('titulo')
        mensagem = self.cleaned_data.get('mensagem')
        if titulo=="" or mensagem=="":
            raise forms.ValidationError(f'Todos os campos são obrigatórios!')

class MensagemFormIndividualUO(forms.Form):
    email = CharField(widget=TextInput(), max_length=255, required=False)
    titulo = CharField(widget=TextInput(), max_length=255, required=False)
    mensagem = CharField(widget=forms.Textarea, max_length=255, required=False)

    def clean(self):
        email = self.cleaned_data.get('email')
        titulo = self.cleaned_data.get('titulo')
        mensagem = self.cleaned_data.get('mensagem')
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError(f'Este email não é válido!')
        if email == "" or titulo=="" or mensagem=="":
            raise forms.ValidationError(f'Todos os campos são obrigatórios!')


class MensagemFormGrupoUO(forms.Form):
    titulo = CharField(widget=TextInput(), max_length=255, required=False)
    mensagem = CharField(widget=forms.Textarea, max_length=255, required=False)
    def clean(self):
        titulo = self.cleaned_data.get('titulo')
        mensagem = self.cleaned_data.get('mensagem')
        if titulo=="" or mensagem=="":
            raise forms.ValidationError(f'Todos os campos são obrigatórios!')


class MensagemFormIndividualParticipante(forms.Form):   
    to = ChoiceField(widget=forms.Select(attrs={'class': "block", 'style':"width: 100%"}))
    titulo = CharField(widget=TextInput(), max_length=255, required=False)
    mensagem = CharField(widget=forms.Textarea, max_length=255, required=False)

    def __init__(self, choices, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['to'].choices = choices

    def clean(self):
        titulo = self.cleaned_data.get('titulo')
        mensagem = self.cleaned_data.get('mensagem')

        if titulo=="" or mensagem=="":
            raise forms.ValidationError(f'Todos os campos são obrigatórios!')


class MensagemFormGrupoParticipante(forms.Form):
    titulo = CharField(widget=TextInput(), max_length=255, required=False)
    mensagem = CharField(widget=forms.Textarea, max_length=255, required=False)
    def clean(self):
        titulo = self.cleaned_data.get('titulo')
        mensagem = self.cleaned_data.get('mensagem')
        if titulo=="" or mensagem=="":
            raise forms.ValidationError(f'Todos os campos são obrigatórios!')






class MensagemResposta(forms.Form):
    mensagem = CharField(widget=forms.Textarea, max_length=255, required=False)
    msg_atual = forms.CharField(widget=forms.HiddenInput())
    def clean(self):
        mensagem = self.cleaned_data.get('mensagem')
        if mensagem=="":
            raise forms.ValidationError(f'A mensagem não pode ser vazia!')
