# LES_PROJETO

Antes de rodar o servidor deverá configurar as credencias da Base de Dados:

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
