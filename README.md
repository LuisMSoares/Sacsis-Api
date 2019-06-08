<h1 align="center">XI SACSIS − Api :hammer_and_wrench:</h1>

- **Projeto desenvolvido com** :package:
   - [Flask-Restful](https://flask-restful.readthedocs.io/en/latest/) - Flask-RESTful is an extension for Flask that adds support for quickly building REST APIs
   - [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) - Flask-SQLAlchemy is an extension for Flask that adds support for SQLAlchemy to your application
   - [Flask-JWT-Extended's](https://flask-jwt-extended.readthedocs.io/) - An open source Flask extension that provides JWT support
   - [Flask-Mail](https://pythonhosted.org/Flask-Mail/) - The Flask-Mail extension provides a simple interface to set up SMTP
   - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/) - A Flask extension for handling Cross Origin Resource Sharing (CORS)
   - [Flask-Excel](https://flask-excel.readthedocs.io/en/latest/) - Flask-Excel is based on pyexcel and makes it easy to consume/produce information stored in excel files over HTTP protocol as well as on file system
   - [Gunicorn](https://gunicorn.org/) - Gunicorn (Green Unicorn) is a Python WSGI HTTP Server for UNIX

### Variaveis de Ambiente :computer::wrench:

| Variavel | Descrição |
| ------ | ------ |
| MASTER_ADM_LOGIN | Login para o administrador mestre (padrão: admin@admin.br) |
| MASTER_ADM_PASSWORD | Senha para o administrador mestre (padrão: admin) |
| SQLALCHEMY_DATABASE_URI | URI de conexão com o banco de dados |
| JWT_SECRET_KEY | Chave secreta para a geração do token |
| JWT_ACCESS_TOKEN_EXPIRES | Quantidade em dias de expiração da sessão do usuário |
| TOKEN_KEY | Chave secreta para a geração do token do formulario de palestras e minicursos |
| MAIL_SERVER | URI do servidor do endereço de email |
| MAIL_PORT | Porta padrão 465 |
| MAIL_USERNAME | Login do servidor de email |
| MAIL_PASSWORD | Senha de login do servidor de email |
| MAIL_DEFAULT_SENDER | Endereço de email do remetente |
| MAIL_USE_TLS | Padrão: false |
| MAIL_USE_SSL | Padrão: true |

### Executando localmente :factory:

Para configurar e executar o projeto de forma automatica e necessario ter o Docker e o Docker Compose previamente instalado. Caso não o possua basta seguir o guia oficial clicando [aqui](https://docs.docker.com/compose/install/)
``` bash
# clonando repositório
$ git clone https://github.com/LuisMSoares/Sacsis-Api
$ cd Sacsis-Api

# instalando dependências e rodando a aplicação
$ docker-compose up --build
```

### Documentação da Api :book:

Acesse a documentação da API clicando [aqui](https://documenter.getpostman.com/view/1867411/S17wP6sV).

### Licença :lock:

Apache-2.0
