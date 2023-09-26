from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,PasswordChangeForm
from django.contrib.auth.models import User
from django.forms import *
from django import forms
from django.contrib.auth.forms import PasswordResetForm
from .models import *



class LoginForm(AuthenticationForm):
    username=CharField(widget=TextInput(attrs={'class':'input','style':''}), label="Nome de Utilizador", max_length=255, required=False)
    password=CharField(widget=PasswordInput(attrs={'class':'input','style':''}), label= 'Senha', max_length=255, required=False)


class UtilizadorRegisterForm(UserCreationForm):

    class Meta:
        model = Utilizador
        fields = ('username', 'password1', 'password2', 'email',
                  'first_name', 'last_name')    
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        erros = []
        if email == "" or first_name=="" or last_name=="" or username=="":
            raise forms.ValidationError(f'Todos os campos são obrigatórios!')

        if username and User.objects.filter(username=username).exists():
            erros.append(forms.ValidationError(f'O username já existe'))

        
        if password1==None or password2==None:
            if password1==None:
                raise forms.ValidationError(f'Todos os campos são obrigatórios!')
            if password2==None:
                raise forms.ValidationError(f'Todos os campos são obrigatórios!')
            else:
                erros.append(forms.ValidationError(f'As palavras-passe não correspondem'))


        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(f'O email já existe')
        elif email==None:
            erros.append(forms.ValidationError(f'O email é inválido'))

  
        if len(erros)>0:
            raise ValidationError([erros])
        


class FuncionarioRegisterForm(UserCreationForm):

    class Meta:
        model = Funcionario
        fields = ('username', 'password1', 'password2', 'email',
                  'first_name', 'last_name')    
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        erros = []
        if email == "" or first_name=="" or last_name=="" or username=="":
            raise forms.ValidationError(f'Todos os campos são obrigatórios!')

        if username and User.objects.filter(username=username).exists():
            erros.append(forms.ValidationError(f'O username já existe'))

        
        if password1==None or password2==None:
            if password1==None:
                raise forms.ValidationError(f'Todos os campos são obrigatórios!')
            if password2==None:
                raise forms.ValidationError(f'Todos os campos são obrigatórios!')
            else:
                erros.append(forms.ValidationError(f'As palavras-passe não correspondem'))


        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(f'O email já existe')
        elif email==None:
            erros.append(forms.ValidationError(f'O email é inválido'))

  
        if len(erros)>0:
            raise ValidationError([erros])





class DocenteRegisterForm(UserCreationForm):
        
    departamentoid = forms.ModelChoiceField(queryset=Departamento.objects.all(), to_field_name='id')
    faculdadeid = forms.ModelChoiceField(queryset=Faculdade.objects.all(), to_field_name='id')
    gabineteid = forms.ModelChoiceField(queryset=Gabinete.objects.all(), to_field_name='id')
    
    class Meta:
        model = Docente
        fields = ('username', 'password1', 'password2', 'email',
                  'first_name', 'last_name','gabineteid','faculdadeid','departamentoid')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['departamentoid'].label_from_instance = lambda obj: obj.nome
        self.fields['faculdadeid'].label_from_instance = lambda obj: obj.nome
        self.fields['gabineteid'].label_from_instance = lambda obj: obj.nome
        

    def clean(self):
        username = self.cleaned_data.get('username')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        gabineteid = self.cleaned_data.get('gabineteid')
        faculdadeid = self.cleaned_data.get('faculdadeid')
        departamentoid = self.cleaned_data.get('departamentoid')


        erros = []
        if email == "" or first_name=="" or last_name=="" or username==None or gabineteid==None or faculdadeid==None or departamentoid==None:
            raise forms.ValidationError(f'Todos os campos são obrigatórios!')

        if username and User.objects.filter(username=username).exists():
            erros.append(forms.ValidationError(f'O username já existe'))

        
        if password1==None or password2==None:
            if password1==None:
                raise forms.ValidationError(f'Todos os campos são obrigatórios!')
            if password1==None:
                raise forms.ValidationError(f'Todos os campos são obrigatórios!')
            else:
                erros.append(forms.ValidationError(f'As palavras-passe não correspondem'))


        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(f'O email já existe')
        elif email==None:
            erros.append(forms.ValidationError(f'O email é inválido'))

        if len(erros)>0:
            raise ValidationError([erros])