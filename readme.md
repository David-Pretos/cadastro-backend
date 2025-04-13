# Cadastro 

Sistema responsável pelo cadastro de usuários, incluindo email, na base de dados coorporativa.

## Requisitos do backend:

- servidor python
- usar flask no servidor
- usar banco de dados sqlite
- 3 rotas:
  - **/cadastrar_usuario**: Rota para cadastrar um novo usuário. Deve receber dados no formato JSON.
  - **/buscar_usuario**: Rota para buscar informações de um usuário pelo ID.
  - **/deletar_usuario**: Rota para deletar um usuário pelo ID.
- deve usar um swagger para documentar as rotas e facilitar o teste da API.


## Versão do python:

- Python 3.12.3

## Ambiente python (opcional):

- Criação: python3 -m venv env_projeto
- Ativação: source env_projeto/bin/activate

## Instalação das dependências do projeto:

- Dependências do projeto no arquivo requirements.txt
- pip install -r requirements.txt

## Para rodar o backend:

- python app.py

## Para rodar o Swagger:

- http://127.0.0.1:5000/swagger


