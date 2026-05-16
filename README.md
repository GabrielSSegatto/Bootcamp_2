# ReservaCinema

API em Flask para gerenciamento de reservas de eventos/sessoes em cinema, com CRUD completo de usuarios, eventos, salas, assentos, sessoes e reservas.

Link do Deploy: https://bootcamp-2-l6ix.onrender.com

## Visao geral

O projeto resolve um problema real de controle de assentos por sessao, impedindo dupla reserva do mesmo assento para a mesma sessao.

Principais recursos:
- Cadastro e gerenciamento de usuarios (com validacao de CPF de 11 digitos)
- Cadastro e gerenciamento de eventos
- Cadastro e gerenciamento de salas
- Cadastro e gerenciamento de assentos por sala
- Cadastro e gerenciamento de sessoes
- Cadastro e gerenciamento de reservas
- Regra critica: bloqueio de reserva duplicada para o mesmo assento na mesma sessao
- Testes automatizados com Pytest
- CI com GitHub Actions

## Tecnologias

- Python 3.9+
- Flask
- Flask-SQLAlchemy
- Flask-Migrate (Alembic)
- SQLite (padrao via `DATABASE_URL`)
- Pytest
- Flake8

## Estrutura do projeto

```text
ReservaCinema/
|- app.py
|- main.py
|- models.py
|- routes.py
|- services.py
|- seed.py
|- validar_requisitos.py
|- requirements.txt
|- VERSION
|- instance/
|- migrations/
|  |- versions/
|- testes/
|  |- test_reservas.py
```

## Pre-requisitos

- Python 3.9, 3.10 ou 3.11
- `pip`

## Configuracao do ambiente

1. Clone o repositorio e entre na pasta do projeto.
2. Crie e ative um ambiente virtual.
3. Instale as dependencias.
4. Configure variaveis de ambiente.

Exemplo:

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

Variaveis esperadas em `.env`:

```env
DATABASE_URL=sqlite:///instance/app.db
SECRET_KEY=sua-chave-secreta-muito-segura-aqui
FLASK_ENV=development
FLASK_APP=app.py
```

## Banco de dados e migracoes

Com o ambiente configurado:

```bash
flask db upgrade
```

Se precisar criar uma nova migracao:

```bash
flask db migrate -m "descricao da migracao"
flask db upgrade
```

## Popular base com dados iniciais (opcional)

```bash
python seed.py
```

O script cria salas, assentos, eventos, sessoes, usuarios e uma reserva inicial.

## Executar a API

```bash
python app.py
```

A API sera iniciada em:
- http://127.0.0.1:5000

## Executar interface CLI (opcional)

```bash
python main.py
```

## Testes

Rodar suite de testes:

```bash
pytest testes/ -v
```

Rodar com cobertura (como na pipeline):

```bash
pytest testes/ -v --cov=services --cov-report=xml
```

## Lint

```bash
flake8 . --max-line-length=100 --exclude=venv,migrations,__pycache__
```

## Endpoints da API

Base URL local: `http://127.0.0.1:5000`

### Usuarios
- `POST /users`
- `GET /users`
- `GET /users/<id>`
- `PUT /users/<id>`
- `DELETE /users/<id>`

Exemplo (criar usuario):

```bash
curl -X POST http://127.0.0.1:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Maria Santos","cpf":"98765432101"}'
```

### Eventos
- `POST /eventos`
- `GET /eventos`
- `GET /eventos/<id>`
- `PUT /eventos/<id>`
- `DELETE /eventos/<id>`

### Salas
- `POST /salas`
- `GET /salas`
- `GET /salas/<id>`
- `PUT /salas/<id>`
- `DELETE /salas/<id>`

### Assentos
- `POST /assentos`
- `GET /assentos`
- `GET /assentos/<id>`
- `PUT /assentos/<id>`
- `DELETE /assentos/<id>`

### Sessoes
- `POST /sessoes`
- `GET /sessoes`
- `GET /sessoes/<id>`
- `PUT /sessoes/<id>`
- `DELETE /sessoes/<id>`

### Reservas
- `POST /reservas`
- `GET /reservas`
- `GET /reservas/<id>`
- `PUT /reservas/<id>`
- `DELETE /reservas/<id>`

Exemplo (criar reserva):

```bash
curl -X POST http://127.0.0.1:5000/reservas \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"sessao_id":1,"assento_id":1}'
```

## Validacoes e regras de negocio

- Usuario:
  - nome e CPF obrigatorios
  - CPF deve conter exatamente 11 digitos numericos
  - CPF unico
- Reserva:
  - user_id, sessao_id e assento_id obrigatorios
  - usuario, sessao e assento devem existir
  - nao permite reservar o mesmo assento duas vezes na mesma sessao
- Remocoes em cascata no nivel de servico:
  - ao remover usuario, remove reservas dele
  - ao remover evento, remove sessoes associadas
  - ao remover sessao, remove reservas associadas
  - ao remover assento, remove reservas associadas
  - ao remover sala, remove sessoes e assentos associados

## Integracao continua

Pipeline em GitHub Actions ([.github/workflows/ci.yml](.github/workflows/ci.yml)) com:
- matriz de Python 3.9, 3.10 e 3.11
- instalacao de dependencias
- lint com Flake8
- testes com Pytest
- geracao/upload de cobertura

## Versao

Versao atual: `1.0.0` (arquivo `VERSION`).

## Licenca

Projeto sob licenca MIT. Veja o arquivo `LICENSE`.
