from app.auth import login, login_required
from app.db import get_db
from flask import (
    Blueprint, render_template, request, redirect, url_for, current_app, g
)
from sqlalchemy import *
from . import db
from .models import Sugerencia

import sendgrid
from sendgrid.helpers.mail import *

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def index():
    return render_template('main/index.html')

@bp.route('/mail', methods=['GET', 'POST'])
def mail():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        new_message = Sugerencia(mensaje=message, id_user=g.user['id'])
        db.session.add(new_message)
        db.session.commit()

        send_mail(name, email, message)

        return redirect(url_for('main.sugerencia_enviada'))

    return render_template('content/suggest.html')

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
    return render_template('main/send_mail.html')

@bp.route('/orden', methods=['GET'])
@login_required
def orden():
    return render_template('content/orden.html')

@bp.route('/seguridad', methods=['GET'])
@login_required
def seguridad():
    return render_template('content/seguridad.html')

@bp.route('/menu', methods=['GET'])
@login_required
def menu():
    return render_template('content/menu.html')
