from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)

class Evento(db.Model):
    __tablename__ = 'eventos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

class Sala(db.Model):
    __tablename__ = 'salas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    capacidade = db.Column(db.Integer, nullable=False)
    cep = db.Column(db.String(8), nullable=False) 

class Sessao(db.Model):
    __tablename__ = 'sessoes'
    id = db.Column(db.Integer, primary_key=True)
    horario_data = db.Column(db.DateTime, nullable=False)
    is_dub = db.Column(db.Boolean, nullable=False)

    evento_id = db.Column(db.Integer, db.ForeignKey('eventos.id'), nullable=False)
    sala_id = db.Column(db.Integer, db.ForeignKey('salas.id'), nullable=False)

    # AS PONTES MÁGICAS (Relationships)
    # Agora o Python consegue acessar s.evento.nome e s.sala.cep sem erro
    evento = db.relationship('Evento', backref='sessoes')
    sala = db.relationship('Sala', backref='sessoes')

class Assento(db.Model):
    __tablename__ = 'assentos'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(10), nullable=False)
    sala_id = db.Column(db.Integer, db.ForeignKey('salas.id'), nullable=False)
    
class Reserva(db.Model):
    __tablename__ = 'reservas'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sessao_id = db.Column(db.Integer, db.ForeignKey('sessoes.id'), nullable=False)
    assento_id = db.Column(db.Integer, db.ForeignKey('assentos.id'), nullable=False)
    data_reserva = db.Column(db.DateTime, default=datetime.now, nullable=False)