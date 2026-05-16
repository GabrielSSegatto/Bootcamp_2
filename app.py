import os
from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

from models import db

app = Flask(__name__)

# --- INÍCIO DA CORREÇÃO PARA O DEPLOY ---
# 1. Pegamos o caminho absoluto da pasta onde o app.py está
basedir = os.path.abspath(os.path.dirname(__file__))

# 2. Definimos o caminho da pasta instance e garantimos que ela exista
instance_path = os.path.join(basedir, 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)


db_path = os.path.join(instance_path, 'cinema.db')

# 4. Configuramos a URI usando o caminho absoluto
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', f'sqlite:///{db_path}')
# --- FIM DA CORREÇÃO ---

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'uma-chave-muito-segura')

db.init_app(app)
migrate = Migrate(app, db)

from routes import bp
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)