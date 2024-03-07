# Aplicação Desenvolvida na cadeira de Laboratório de Engenharia de Software(LES)

Este projeto visa solucionar uma aplicação Web que conte com um design simples, intuitivo e limpo, de maneira que os utilizadores consigam gerir os pedidos sem complicações e de forma muito mais eficaz e fácil.
A aplicação web permite aos docentes registar seus pedidos, receber notificações sobre o estado e obter respostas do CP. Os funcionários do CP puderam visualizar os pedidos recebidos, pesquisar e marcá-los como em análise, rejeitados ou aprovados, além de enviar respostas por e-mail aos docentes. A interação entre docentes e funcionários foi facilitada, e a aplicação possibilitou o envio de mensagens via e-mail para a Presidenta do CP, quando necessário.
Este trabalho foi realizado por:   
- Kartic Hitendra Premgi
- Diogo Afonso Nobre Zacarias
- Daniel Ferros Fernandes
- João Pedro Gomes de Almeida

Antes de rodar o aplicação deverá configurar as credencias da Base de Dados:

Pasta: gestaodepedidos

Ficheiro: settings.py

Deverá colocar no lugar do USER e PASSWORD, as suas credencias de acesso ao PHPmyadmin

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'les_grupo2',
            'USER': 'a71379',
            'PASSWORD': '1234',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }

De seguida, deverá importar o ficheiro bd.sql , e desativar no momento o botão "Ativa a verificação de chaves estrangeiras"

De seguida, terá que instalar as bibliotecas necessarias poderá fazer 
    
    make install

ou

    pip install -r requirements.txt

Para rodar o servidor terá que fazer o seguinte comando:

    make run

ou 

    python manage.py runserver



Credencias de acesso para o Docente:

    User: Docente
    Password: Funcionario


Credencias de acesso para o Funcionario:

    User: Funcionario
    Password: Docentes

Credencias de acesso para o PCP:

    User: dan23
    Password: caoladrao12

Credencias de acesso para o Professora:

    User: paula12
    Password: admin123admin

Prints da APP:

- HomePage:
  ![imagem](https://github.com/Kartic23/Gestao-de-Pedidos/assets/105547398/3b7e7a64-fc4b-40f8-aa81-2f16b6281a9f)

- Register:
  ![imagem](https://github.com/Kartic23/Gestao-de-Pedidos/assets/105547398/f4339dfe-4e9b-4dfb-a530-5ecfaf63efe6)

- Login:
  ![imagem](https://github.com/Kartic23/Gestao-de-Pedidos/assets/105547398/7e5c1c9f-9447-494c-9a11-402e8d212bc9)
  
- Listar Pedidos:
  ![imagem](https://github.com/Kartic23/Gestao-de-Pedidos/assets/105547398/4ed1268f-1058-4b0c-8e2a-dbdb7eaab645)

  
- Criar Pedidos:
- 

