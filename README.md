# iClinic API

Projeto de desafio para a vaga de Python Backend Developer na iClinic. A descrição do desafio está no arquivo README_iclinic.md

Esse projeto é hosteado no Heroku e pode ser acessado a partir da URL https://iclinic-desafio.herokuapp.com

## Documentação
A documentação da API está disponível em (TODO)

## Como executar locamente
1. instalar o Docker e o docker-compose
2. clonar o repositório
3. adicionar .env na raíz do projeto (descrição completa das variáveis no arquivo env-exemplo)
    - .env
    - db.env
    - api.env
4. executar o comando: 
```bash
docker-compose up
```

## Como executar testes unitários
```bash
python3 manage.py test
```

### Coverage
```bash
coverage run --source='.' manage.py test api && coverage report
```