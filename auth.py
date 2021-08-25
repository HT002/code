import functools
from operator import or_, and_
from flask_login import login_user, logout_user, login_required, current_user
from flask import (
    Blueprint, flash, g, render_template, request, url_for, redirect
)
from sqlalchemy import *
from werkzeug.security import check_password_hash, generate_password_hash
from . import db
from .models import Personal, User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        correo = request.form['correo']
        tim = request.form['tim']
        password = request.form['password']
        password_2 = request.form['password_repeat']
    
        correo_exists = Personal.query.filter_by(correo=correo).first()
        tim_exists = Personal.query.filter_by(tim=tim).first()

        if correo_exists:
            if tim_exists:
                user_exists = User.query.filter_by(id_personal=tim_exists.id).first()
                if user_exists is None:
                    if password == password_2:
                        new_user = User(password=generate_password_hash(password), id_personal=tim_exists.id)
                        db.session.add(new_user)
                        db.session.commit()
                        login_user(new_user, remember=True)
                        flash('Usuario creado con éxito.', category='success')
                        return redirect(url_for('main.index'))
                    else:
                        flash('Las contraseñas no coinciden.', category='error')
                else:
                    flash('Ya existe un usuario enlazado a ese correo y esa TIM.', category='error')
            else:
                flash('La TIM o el correo no consta en la base de datos de la unidad.', category='error')
        else:
            flash('La TIM o el correo no consta en la base de datos de la unidad.', category='error')

    return render_template('auth/register.html', user=current_user)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']

        my_personal = Personal.query.filter(or_(
                Personal.correo==usuario, Personal.tim==usuario)
        ).first()
        
        if my_personal:
            my_user = User.query.filter_by(id_personal=my_personal.id).first()
            if my_user:
                if check_password_hash(my_user.password, password):
                    flash('Inicio de sesión exitoso.', category='success')
                    login_user(my_user, remember=True)
                    return redirect(url_for('main.index'))
                else:
                    flash('Credenciales de acceso incorrectas', category='error')
            else:
                flash('Credenciales de acceso incorrectas', category='error')
        else:
            flash('Credenciales de acceso incorrectas', category='error')

    return render_template('auth/login.html', user=current_user)

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))

@bp.before_app_request
def load_logged_in_user():
    if current_user is None:
        g.personal = None
    else:
        my_personal = Personal.query.filter(Personal.id==current_user.id_personal).first()
        g.personal = my_personal