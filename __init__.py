from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SENDGRID_KEY=os.environ.get('SENDGRID_KEY'),
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI'),
        SQLALCHEMY_TRACK_MODIFICATIONS=os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS'),
    )

    db.init_app(app)

    from .models import User

    create_database(app)

    from . import auth

    app.register_blueprint(auth.bp)

    from . import data

    app.register_blueprint(data.bp)

    from . import main

    app.register_blueprint(main.bp)

    return app

def create_database(app):
    pass
    # if not path.exists("website/" + DB_NAME):
    # db.create_all(app=app)
    # print("Created database!")