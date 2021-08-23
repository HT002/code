import functools

from flask import (
    Blueprint, flash, g, render_template, request, url_for, session, redirect
)

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect

from . import db
from .models import user

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        correo = request.form['correo']
        tim = request.form['tim']
        password = request.form['password']
        password_2 = request.form['password_repeat']
        
        


        new_user = user(password=password)
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
        db, c = get_db()
        error = None
        c.execute(
            """
            select 
                u.password,
                u.id
            from personal p 
            inner join user u on u.id_personal = p.id
            where 
                p.tim = %s or p.correo = %s
            """, (correo, correo)
        )
        user = c.fetchone()

        if user is None:
            error = 'Credenciales de acceso incorrectas'
        elif not check_password_hash(user['password'], password):
            error = 'Credenciales de acceso incorrectas'
        
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
        g.personal = None
    else:
        db, c = get_db()
        c.execute(
            'select * from user where id = %s', (user_id,)
        )
        g.user = c.fetchone()

        c.execute(
            'select * from personal where id = %s', (g.user['id_personal'],)
        )
        g.personal = c.fetchone()
           
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