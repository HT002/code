from app.auth import login
from app.auth import login_required
from flask import (
    Blueprint, render_template, request, redirect, url_for, current_app
)
import sendgrid
from sendgrid.helpers.mail import *

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def index():
    return render_template('main/index.html')

@bp.route('/mail', methods=['GET', 'POST'])
def mail():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if request.method == 'POST':
        send_mail(name, email, message)
        return render_template('main/send_mail.html')

    return redirect(url_for('main.index'))

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
        <p>Hola Buner, tienes un nuevo contacto desde la web:</p>
        <p>Nombre: -name-</p>
        <p>Correo: -email-</p>
        <p>Mensaje: -message-</p>
    """
    
    mail = Mail(mi_email, to_email, 'Nuevo contacto desde la web', html_content=html_content)
    response = sg.client.mail.send.post(request_body=mail.get())

@bp.route('/principal', methods=['GET'])
@login_required
def start():
    return render_template('content/start.html')

@bp.route('/sugerencias', methods=['GET'])
@login_required
def sugerencias():
    return render_template('content/suggest.html')

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
