from app.auth import login, login_required
from flask_login import login_user, logout_user, login_required, current_user
from flask import (
    Blueprint, render_template, request, redirect, url_for, current_app, g
)
from operator import or_, and_
from sqlalchemy import *
from . import db
from .models import Sugerencia, User, Personal

import sendgrid
from sendgrid.helpers.mail import *

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def index():
    
    return render_template('main/index.html', user=current_user)

@bp.route('/mail', methods=['GET', 'POST'])
def mail():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        my_personal = Personal.query.filter(Personal.nombre==name).first()
        my_user = User.query.filter(User.id_personal==my_personal.id).first()

        new_message = Sugerencia(mensaje=message, id_user=my_user.id)
        db.session.add(new_message)
        db.session.commit()

        send_mail(name, email, message)

        return redirect(url_for('main.sugerencia_enviada'))

    return render_template('content/suggest.html', user=current_user)

def send_mail(name, email, message):
    mi_email = 'rubns_73@hotmail.com'
    sg = sendgrid.SendGridAPIClient(api_key=current_app.config['SENDGRID_KEY'])

    from_email = Email(mi_email)
    to_email = To(mi_email, substitutions={
        "-name-": name,
        "-email-": email,
        "-message-": message,
    })

    html_content = """
        <p>Hola Rubén, tienes un nuevo contacto desde la web:</p>
        <p>Nombre: -name-</p>
        <p>Correo: -email-</p>
        <p>Mensaje: -message-</p>
    """
    
    mail = Mail(mi_email, to_email, 'Nuevo contacto desde la web', html_content=html_content)
    response = sg.client.mail.send.post(request_body=mail.get())


@bp.route('/Sugerencia enviada', methods=['GET'])
@login_required
def sugerencia_enviada():
    return render_template('main/send_mail.html', user=current_user)

@bp.route('/orden', methods=['GET'])
@login_required
def orden():
    return render_template('content/orden.html', user=current_user)

@bp.route('/seguridad', methods=['GET'])
@login_required
def seguridad():
    return render_template('content/seguridad.html', user=current_user)

@bp.route('/menu', methods=['GET'])
@login_required
def menu():
    return render_template('content/menu.html', user=current_user)
