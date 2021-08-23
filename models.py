from datetime import timezone
from enum import unique
from . import db
from sqlalchemy.sql import func

class Personal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tim = db.Column(db.String(10), nullable=False, unique=True)
    nombre = db.Column(db.String(20), nullable=False)
    apellido = db.Column(db.String(20), nullable=False)
    correo = db.Column(db.String(50), nullable=False, unique=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(500), nullable=False)
    id_personal = db.Column(db.Integer, db.ForeignKey('personal.id'), nullable=False, unique=True)

class Deporte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identificador_deporte = db.Column(db.String(20), nullable=False, unique=True)

class Zona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identificador_zona = db.Column(db.String(20), nullable=False)
    id_deporte = db.Column(db.Integer, db.ForeignKey('deporte.id'),nullable=False)

class Dia_comida(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False, unique=True)

class Turno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_turno = db.Column(db.String(10), nullable=False)
    id_dia_comida = db.Column(db.Integer, db.ForeignKey('dia_comida.id'), nullable=False)

class Reserva_deporte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False, unique=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_zona = db.Column(db.Integer, db.ForeignKey('zona.id'), nullable=False)

class Reserva_comida(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_turno = db.Column(db.Integer, db.ForeignKey('turno.id'), nullable=False)

class Sugerencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mensaje = db.Column(db.String(500), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)