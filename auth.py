import functools

from flask import (
    Blueprint, flash, g, render_template, request, url_for, session, redirect
)
from sqlalchemy import *
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect

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
        error = None
        
        """
        personal_exists = Personal.query.filter(and_(
            Personal.correo==correo, Personal.tim==tim)
        ).first()
        user_exists = User.query.filter_by(id_personal=personal_exists.id)
        """

        correo_exists = Personal.query.filter_by(correo=correo).first()
        tim_exists = Personal.query.filter_by(tim=tim).first()
        user_exists = User.query.filter_by(id=tim_exists.id).first()

        if not correo:
            error = 'Correo corporativo es requerido'
        elif not tim:
            error = 'TIM es requerida'
        elif not password:
            error = 'Contraseña es requerida'
        elif correo_exists is None:
            error = 'El correo corporativo "{}" no consta en la base de datos de la unidad.'.format(correo)
        elif tim_exists is None:
            error = 'La TIM "{}" no consta en la base de datos de la unidad.'.format(tim)
        elif user_exists:
            error = 'Ya existe un usuario registrado que está enlazado a ese correo y esa TIM.'
        elif password != password_2:
            error = 'Las contraseñas no coinciden.'
        
        if error is None:
            new_user = User(password=generate_password_hash(password), id_personal=tim_exists.id)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        
        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']
        error = None

        my_personal = Personal.query.filter(or_(
                Personal.correo==correo, Personal.tim==correo)
        ).first()
        my_user = User.query.filter_by(id_personal=my_personal.id).first()
        # raise Exception(my_user.id_Personal)
            
        
        
        
        if my_personal is None:
            error = 'Credenciales de acceso incorrectas'
        elif not check_password_hash(User['password'], password):
            error = 'Credenciales de acceso incorrectas'
        
        if error is None:
            session.clear()
            session['user_id'] = User['id']
            return redirect(url_for('main.index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
        g.Personal = None
    else:

        my_user = User.query.filter_by(id=user_id).first()
        raise Exception(my_user.id_Personal)
        g.user = my_user
        g.Personal = my_user.id_Personal
        """
        db, c = get_db()
        c.execute(
            'select * from user where id = %s', (user_id,)
        )
        g.user = c.fetchone()

        c.execute(
            'select * from Personal where id = %s', (g.user['id_Personal'],)
        )
        g.Personal = c.fetchone()
        """ 

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))