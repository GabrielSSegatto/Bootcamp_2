# ReservaCinema - Entrega Final (Bootcamp)

API em Flask para gerenciamento de reservas de eventos/sessões em cinema, com CRUD completo.
**Link do Deploy:** https://bootcamp-2-l6ix.onrender.com

## 👥 Equipe de Desenvolvimento
* **Gabriel Soares Segatto** - Matrícula: [22502904] - github: GabrielSSegatto

* **João Gabriel de Moura Torres** - Matrícula: [22503395] - github: Joaooh

* **André Yuri Alves Silva** - Matrícula: [2250984301] - github: yurial3445

* **Gabriel Caramez Benvindo da Silva** - Matrícula: [22504116] - github: GabrielCaramez

* **Nicolas Klaczko Hogan** - Matrícula: [22506264] - github: NicolasKlaczkoHogan

## 🚀 Visão geral
O projeto resolve um problema real de controle de assentos por sessão, impedindo dupla reserva. Na etapa final, a aplicação foi migrada de um banco de dados local para uma arquitetura em nuvem, trabalhando em equipe via Pull Requests.

**Principais recursos:**
* Integração com Banco de Dados Relacional em Nuvem (**Supabase/PostgreSQL**).
* Integração com API externa (**ViaCEP**) para localização de salas.
* Regra crítica: bloqueio de reserva duplicada para o mesmo assento/sessão.
* Testes automatizados com Pytest rodando em Pipeline CI/CD (GitHub Actions).

## 🛠️ Tecnologias
* Python 3.9+
* Flask & Flask-SQLAlchemy
* PostgreSQL (Supabase DBaaS)
* Flask-Migrate (Alembic)
* Pytest & Flake8

## ⚙️ Como rodar o projeto localmente
Clone o repositório, crie um ambiente virtual e instale as dependências:
```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
