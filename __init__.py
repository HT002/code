from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from os import path

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:rootttxd7@localhost/academia'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.config.from_mapping(
        SENDGRID_KEY=os.environ.get('SENDGRID_KEY'),
        SECRET_KEY=os.environ.get('SECRET_KEY'),
    )

    from . import main
    from . import auth
    from . import data

    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(data.bp)

    from .models import User, Personal, Deporte, Reserva_comida, Reserva_deporte, Zona, Dia_comida, Turno, Sugerencia

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    pass
    # if not path.exists("website/" + DB_NAME):
    #db.create_all(app=app)
    #print("Created database!")