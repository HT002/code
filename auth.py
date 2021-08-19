import functools

from flask import (
    Blueprint, flash, g, render_template, request, url_for, session, redirect
)

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect

from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        correo = request.form['correo']
        tim = request.form['tim']
        password = request.form['password']
        db, c = get_db()
        error = None
        c.execute(
            'select id from user where tim = %s', (tim,)
        )
        if not correo:
            error = 'Correo corporativo es requerido'
        if not tim:
            error = 'TIM es requerida'
        if not password:
            error = 'Contraseña es requerida'
        elif c.fetchone() is not None:
            error = 'El usuario con TIM {} ya existe.'.format(tim)

        c.execute(
            'select tim from personal where tim = %s', (tim,)
        )
        if c.fetchone() is None:
            error = 'La TMI {} no consta en base de datos corporativa.'.format(tim)
        
        c.execute(
            'select email from correo where email = %s', (correo,)
        )
        if c.fetchone() is None:
            error = 'El correo {} no consta en la base de datos corporativa.'.format(correo)

        if error is None:
            c.execute(
                'insert into user (tim, password) values (%s, %s)', (tim, generate_password_hash(password))
            )
            db.commit()

            c.execute(
            'select * from user where tim = %s', (tim,)
            )
            user = c.fetchone()
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('main.index'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        tim = request.form['tim']
        password = request.form['password']
        db, c = get_db()
        error = None
        c.execute(
            'select * from user where tim = %s', (tim,)
        )
        user = c.fetchone()

        if user is None:
            error = 'Usuario o contraseña incorrecto'
        elif not check_password_hash(user['password'], password):
            error = 'Usuario o contraseña incorrecto'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('main.index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute(
            'select * from user where id = %s', (user_id,)
        )
        g.user = c.fetchone()
           
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