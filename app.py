import os
from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv

# Carregando as variáveis de ambiente do arquivo .env
load_dotenv()

# Importa a instância do banco
from models import db

# Criando a aplicação Flask
app = Flask(__name__)

# CONFIGURAÇÃO DO BANCO DE DADOS
# Ajustado para apontar para a pasta instance/cinema.db como fallback
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///instance/cinema.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Chave secreta com fallback para segurança do deploy
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'uma-chave-muito-segura-e-secreta')

# Conecta o bd e as migrations com a aplicação
db.init_app(app)
migrate = Migrate(app, db)

# Importando as rotas
from routes import bp
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)