# Sacsis-Api

Api para a aplicação web SACSIS XI

## Rotas da Api

### Cadastro de usuário

#### Request

    POST: https://sacsis-api.herokuapp.com/api/user
Json data

    {
       'nome':'usuário teste',
       'email': 'usario@teste',
       'matricula': '1234',
       'cpf': '01234567891',
       'rg': '1111111111111',
       'senha': 'teste123'
    }
    
#### Response status code

Endereço de email duplicado `422`

    {
       'message':'Endereço de email já cadastrado'
    }
    
Cadastrado com sucesso `201`

    {
       'message':'Usuário cadastrado'
    }



### Login

#### Request

    POST: https://sacsis-api.herokuapp.com/api/login
Json data

    {
       'login':'usario@teste',
       'senha': 'teste123'
    }
    
#### Response status code

Login não encontrado `401`

    {
       'message':'Login para o usuario não encontrado'
    }
Senha incorreta `401`

    {
       'message':'Senha informada incorreta'
    }
Login efetuado com sucesso `200`

    {
       'jwt_token':'um_token_gerado'
    }
 

<<<<<<< HEAD

=======
>>>>>>> develop
