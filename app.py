import os
from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

from models import db

app = Flask(__name__)


database_url = os.getenv('DATABASE_URL')

if not database_url:
    raise ValueError("A variável DATABASE_URL não foi encontrada no .env!")

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'uma-chave-muito-segura')

db.init_app(app)
migrate = Migrate(app, db)

from routes import bp
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)